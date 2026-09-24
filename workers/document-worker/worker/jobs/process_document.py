import logging
from uuid import UUID

from app.ai.embeddings.factory import get_embedding_provider
from app.core.config import get_settings
from app.document_processing.chunking.structure_aware import StructureAwareChunker
from app.document_processing.metadata.page_mapper import infer_logical_page
from app.infrastructure.database.session import SessionLocal
from app.infrastructure.storage.minio import MinioObjectStorage
from app.infrastructure.vectorstore.qdrant import QdrantVectorStore
from app.modules.documents.models import (
    Document,
    DocumentChunk,
    DocumentPage,
    ProcessingJob,
)
from app.shared.enums import DocumentStatus
from sqlalchemy import delete
from worker.jobs.extract_pages import extract_pages
from worker.jobs.generate_embeddings import generate_embeddings
from worker.jobs.index_document import index_document

logger = logging.getLogger(__name__)


def _update_job(
    session, document_id: UUID, stage: str, status: str | None = None
) -> None:
    job = (
        session.query(ProcessingJob)
        .filter(ProcessingJob.document_id == document_id)
        .order_by(ProcessingJob.created_at.desc())
        .first()
    )
    if job:
        job.stage = stage
        if status:
            job.status = status
            if status == "running":
                job.attempts += 1


async def process_document(_: dict, document_id: str) -> None:
    """Persist provenance before vector indexing; a failure never marks a document ready."""
    settings = get_settings()
    session = SessionLocal()
    identifier = UUID(document_id)
    try:
        document = session.get(Document, identifier)
        if not document:
            logger.warning("document_missing", extra={"document_id": document_id})
            return
        document.status = DocumentStatus.PROCESSING.value
        _update_job(session, identifier, "extracting", "running")
        session.commit()

        source = MinioObjectStorage.from_settings(settings).download(
            document.storage_key
        )
        pages = extract_pages(source)
        chunker = StructureAwareChunker(
            settings.chunk_size_tokens, settings.chunk_overlap_tokens
        )
        drafts = chunker.chunk(pages)
        drafts = [
            draft.__class__(
                physical_page=draft.physical_page,
                logical_page=infer_logical_page(pages[draft.physical_page - 1]),
                chunk_key=draft.chunk_key,
                text=draft.text,
                heading=draft.heading,
                section=draft.section,
                bbox=draft.bbox,
                token_count=draft.token_count,
                extraction_method=draft.extraction_method,
            )
            for draft in drafts
        ]
        _update_job(session, identifier, "persisting_pages")
        session.execute(
            delete(DocumentPage).where(DocumentPage.document_id == identifier)
        )
        session.execute(
            delete(DocumentChunk).where(DocumentChunk.document_id == identifier)
        )
        for page in pages:
            session.add(
                DocumentPage(
                    document_id=identifier,
                    physical_page=page.physical_page,
                    logical_page=infer_logical_page(page),
                    extracted_text=page.text,
                    extraction_method=page.extraction_method,
                    text_quality_score=page.text_quality_score,
                    dimensions={"width": page.width, "height": page.height},
                )
            )
        chunks = [
            DocumentChunk(
                document_id=identifier,
                physical_page=draft.physical_page,
                logical_page=draft.logical_page,
                chunk_key=draft.chunk_key,
                text=draft.text,
                heading=draft.heading,
                section=draft.section,
                bbox=draft.bbox,
                token_count=draft.token_count,
                extraction_method=draft.extraction_method,
            )
            for draft in drafts
        ]
        session.add_all(chunks)
        document.page_count = len(pages)
        session.flush()

        _update_job(session, identifier, "embedding")
        session.commit()
        vectors = generate_embeddings(drafts, get_embedding_provider())
        _update_job(session, identifier, "indexing")
        session.commit()
        index_document(
            document,
            chunks,
            vectors,
            QdrantVectorStore(
                str(settings.qdrant_url),
                settings.qdrant_collection,
                settings.embedding_dimension,
            ),
        )

        document.status = DocumentStatus.READY.value
        document.failure_reason = None
        _update_job(session, identifier, "complete", "completed")
        session.commit()
    except Exception as error:
        session.rollback()
        document = session.get(Document, identifier)
        if document:
            document.status = DocumentStatus.FAILED.value
            document.failure_reason = (
                "Processing failed. See protected server logs for the technical cause."
            )
            _update_job(session, identifier, "failed", "failed")
            job = (
                session.query(ProcessingJob)
                .filter(ProcessingJob.document_id == identifier)
                .order_by(ProcessingJob.created_at.desc())
                .first()
            )
            if job:
                job.error_message = str(error)[:2000]
            session.commit()
        logger.exception(
            "document_processing_failed", extra={"document_id": document_id}
        )
        raise
    finally:
        session.close()
