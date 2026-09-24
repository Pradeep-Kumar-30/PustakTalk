from abc import ABC, abstractmethod

from app.shared.types import ChunkEvidence


class Reranker(ABC):
    @abstractmethod
    def rerank(
        self, query: str, evidence: list[ChunkEvidence], limit: int
    ) -> list[ChunkEvidence]: ...
