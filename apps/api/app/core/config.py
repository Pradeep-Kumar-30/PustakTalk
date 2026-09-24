from functools import lru_cache
from typing import Literal

from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Typed settings. Environment is read in one place only."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: Literal["development", "test", "production"] = "development"
    app_url: str = "http://localhost:3000"
    api_url: str = "http://localhost:8000"
    log_level: str = "INFO"
    auth_secret: str = Field(min_length=16, default="local-development-secret-change-me")
    auth_cookie_secure: bool = False
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"
    database_url: str = "sqlite:///./pustaktalk.db"
    redis_url: str = "redis://localhost:6379/0"
    qdrant_url: AnyHttpUrl = "http://localhost:6333"
    qdrant_collection: str = "pustaktalk_chunks"
    minio_endpoint: str = "localhost:9000"
    minio_access_key: str = "pustaktalk"
    minio_secret_key: str = "pustaktalk"
    minio_bucket: str = "pustaktalk-documents"
    minio_secure: bool = False
    install_ai: bool = False
    ollama_base_url: AnyHttpUrl = "http://localhost:11434"
    llm_model: str = "qwen3:0.6b"
    embedding_model: str = "intfloat/multilingual-e5-small"
    embedding_dimension: int = Field(default=384, ge=64, le=4096)
    reranker_model: str = "BAAI/bge-reranker-v2-m3"
    enable_reranker: bool = False
    whisper_model: str = "small"
    whisper_device: str = "cpu"
    whisper_compute_type: str = "int8"
    tts_provider: Literal["piper"] = "piper"
    piper_voice: str = "en_US-lessac-medium"
    piper_hindi_voice: str = "hi_IN-pratham-medium"
    piper_data_dir: str | None = "/models/piper"
    max_upload_bytes: int = Field(default=52_428_800, gt=0)
    rate_limit_per_minute: int = Field(default=60, gt=0)
    chunk_size_tokens: int = Field(default=420, ge=100, le=1500)
    chunk_overlap_tokens: int = Field(default=60, ge=0, le=400)

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
