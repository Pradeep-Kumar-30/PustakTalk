from uuid import UUID

from app.modules.documents.repository import DocumentRepository


class LexicalRetriever:
    def __init__(self, documents: DocumentRepository) -> None:
        self._documents = documents

    def search(self, query: str, workspace_id: UUID, limit: int) -> dict[UUID, float]:
        chunks = self._documents.search_lexical(workspace_id, query, limit)
        return {chunk.id: 1.0 / (index + 1) for index, chunk in enumerate(chunks)}
