from dataclasses import replace

from sentence_transformers import CrossEncoder

from app.ai.reranking.base import Reranker
from app.shared.types import ChunkEvidence


class LocalReranker(Reranker):
    def __init__(self, model_name: str) -> None:
        self._model = CrossEncoder(model_name)

    def rerank(self, query: str, evidence: list[ChunkEvidence], limit: int) -> list[ChunkEvidence]:
        if not evidence:
            return []
        scores = self._model.predict([(query, item.text) for item in evidence])
        ranked = [
            replace(item, score=float(score)) for item, score in zip(evidence, scores, strict=True)
        ]
        return sorted(ranked, key=lambda item: item.score, reverse=True)[:limit]
