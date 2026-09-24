from functools import lru_cache

from app.ai.llm.base import LLMProvider
from app.ai.llm.ollama import OllamaProvider
from app.core.config import get_settings


@lru_cache
def get_llm_provider() -> LLMProvider:
    settings = get_settings()
    return OllamaProvider(str(settings.ollama_base_url), settings.llm_model)
