from uuid import UUID

from app.ai.embeddings.base import EmbeddingProvider
from app.infrastructure.vectorstore.base import VectorStore


class DenseRetriever:
    def __init__(self, embeddings: EmbeddingProvider, vectors: VectorStore) -> None:
        self._embeddings = embeddings
        self._vectors = vectors

    def search(self, query: str, workspace_id: UUID, limit: int) -> dict[UUID, float]:
        matches = self._vectors.search(self._embeddings.embed_query(query), workspace_id, limit)
        return {match.id: match.score for match in matches}
