from functools import lru_cache

from app.ai.embeddings.base import EmbeddingProvider
from app.core.config import get_settings
from app.core.exceptions import ServiceUnavailableError


@lru_cache
def get_embedding_provider() -> EmbeddingProvider:
    # Loading sentence-transformers is deliberately deferred until a chat request
    # needs embeddings.  This keeps API health, authentication, and document
    # management available while a local model is being installed or repaired.
    try:
        from app.ai.embeddings.local import LocalEmbeddingProvider
    except ModuleNotFoundError as error:
        raise ServiceUnavailableError(
            "Local AI dependencies are not installed. Set INSTALL_AI=true and rebuild "
            "the API and worker images."
        ) from error

    return LocalEmbeddingProvider(get_settings().embedding_model)
