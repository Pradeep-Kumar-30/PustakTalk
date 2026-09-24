import logging
from uuid import UUID

from app.ai.reranking.base import Reranker
from app.ai.retrieval.hybrid import HybridRetriever
from app.modules.chat.repository import ChatRepository
from app.shared.types import ChunkEvidence

logger = logging.getLogger(__name__)


class RagPipeline:
    def __init__(
        self, retriever: HybridRetriever, repository: ChatRepository, reranker: Reranker | None
    ) -> None:
        self._retriever = retriever
        self._repository = repository
        self._reranker = reranker

    def retrieve(
        self, query: str, workspace_id: UUID, allowed_document_ids: set[UUID] | None, limit: int = 8
    ) -> list[ChunkEvidence]:
        try:
            fused = self._retriever.search(query, workspace_id, limit=20)
        except Exception as error:
            logger.warning(
                "dense_retrieval_unavailable", extra={"error_type": type(error).__name__}
            )
            fused = []
        evidence = self._repository.hydrate_evidence(fused, allowed_document_ids)
        if not evidence:
            # The lexical fallback remains useful when the vector service/model
            # is temporarily unavailable.
            evidence = self._repository.hydrate_evidence(
                self._retriever.lexical_search(query, workspace_id, 20), allowed_document_ids
            )
        if self._reranker and evidence:
            try:
                evidence = self._reranker.rerank(query, evidence, limit)
            except Exception as error:
                logger.warning("reranking_unavailable", extra={"error_type": type(error).__name__})
                evidence = evidence[:limit]
        return evidence[:limit]
