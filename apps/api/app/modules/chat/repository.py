from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.chat.models import Citation, Message
from app.modules.documents.models import Document, DocumentChunk
from app.shared.types import ChunkEvidence


class ChatRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add_message(self, message: Message) -> Message:
        self._session.add(message)
        self._session.flush()
        return message

    def hydrate_evidence(
        self, scores: Sequence[tuple[UUID, float]], allowed_document_ids: set[UUID] | None
    ) -> list[ChunkEvidence]:
        identifiers = [identifier for identifier, _ in scores]
        if not identifiers:
            return []
        rows = self._session.execute(
            select(DocumentChunk, Document).join(Document).where(DocumentChunk.id.in_(identifiers))
        ).all()
        by_id = {chunk.id: (chunk, document) for chunk, document in rows}
        result: list[ChunkEvidence] = []
        for identifier, score in scores:
            row = by_id.get(identifier)
            if not row:
                continue
            chunk, document = row
            if allowed_document_ids and document.id not in allowed_document_ids:
                continue
            result.append(
                ChunkEvidence(
                    chunk_id=chunk.id,
                    document_id=document.id,
                    document_name=document.original_filename,
                    physical_page=chunk.physical_page,
                    logical_page=chunk.logical_page,
                    text=chunk.text,
                    bbox=chunk.bbox,
                    section=chunk.section,
                    score=score,
                    metadata={
                        "heading": chunk.heading,
                        "extraction_method": chunk.extraction_method,
                    },
                )
            )
        return result

    def persist_citations(self, message_id: UUID, evidence: list[ChunkEvidence]) -> list[Citation]:
        citations = [
            Citation(
                message_id=message_id,
                document_id=item.document_id,
                chunk_id=item.chunk_id,
                document_name=item.document_name,
                physical_page=item.physical_page,
                logical_page=item.logical_page,
                source_text=item.text,
                bbox=item.bbox,
            )
            for item in evidence
        ]
        self._session.add_all(citations)
        self._session.flush()
        return citations
