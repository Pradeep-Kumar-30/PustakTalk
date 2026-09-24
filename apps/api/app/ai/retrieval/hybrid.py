from uuid import UUID

from app.ai.retrieval.dense import DenseRetriever
from app.ai.retrieval.fusion import reciprocal_rank_fusion
from app.ai.retrieval.lexical import LexicalRetriever


class HybridRetriever:
    def __init__(self, dense: DenseRetriever, lexical: LexicalRetriever) -> None:
        self._dense = dense
        self._lexical = lexical

    def search(self, query: str, workspace_id: UUID, limit: int = 20) -> list[tuple[UUID, float]]:
        return reciprocal_rank_fusion(
            [
                self._dense.search(query, workspace_id, limit),
                self._lexical.search(query, workspace_id, limit),
            ]
        )[:limit]

    def lexical_search(
        self, query: str, workspace_id: UUID, limit: int = 20
    ) -> list[tuple[UUID, float]]:
        return list(self._lexical.search(query, workspace_id, limit).items())
