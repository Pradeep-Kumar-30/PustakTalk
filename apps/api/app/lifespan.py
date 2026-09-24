from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import bootstrap  # noqa: F401
from app.core.config import get_settings
from app.infrastructure.database.base import Base
from app.infrastructure.database.session import engine
from app.infrastructure.storage.minio import MinioObjectStorage


@asynccontextmanager
async def lifespan(_: FastAPI):
    settings = get_settings()
    if settings.app_env in {"development", "test"}:
        Base.metadata.create_all(bind=engine)
    if settings.app_env != "test":
        MinioObjectStorage.from_settings(settings).ensure_bucket()
    yield
