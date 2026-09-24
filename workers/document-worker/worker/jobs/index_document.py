from app.infrastructure.vectorstore.base import VectorRecord, VectorStore
from app.modules.documents.models import Document, DocumentChunk


def index_document(
    document: Document,
    chunks: list[DocumentChunk],
    vectors: list[list[float]],
    store: VectorStore,
) -> None:
    store.upsert(
        [
            VectorRecord(
                id=chunk.id,
                vector=vector,
                payload={
                    "workspace_id": str(document.workspace_id),
                    "document_id": str(document.id),
                    "physical_page": chunk.physical_page,
                    "section": chunk.section,
                },
            )
            for chunk, vector in zip(chunks, vectors, strict=True)
        ]
    )
