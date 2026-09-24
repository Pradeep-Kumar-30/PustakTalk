from functools import lru_cache

from app.ai.reranking.base import Reranker
from app.core.config import get_settings


@lru_cache
def get_reranker() -> Reranker:
    # CrossEncoder is an optional, resource-intensive local model.  Avoid
    # importing it on API startup when reranking is disabled (the default).
    from app.ai.reranking.local import LocalReranker

    return LocalReranker(get_settings().reranker_model)
