import logging

from fastapi import APIRouter, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.core.config import get_settings
from app.core.exceptions import DomainError
from app.core.logging import configure_logging
from app.core.middleware import RequestContextMiddleware
from app.core.security_headers import SecurityHeadersMiddleware
from app.infrastructure.cache.rate_limit import RedisRateLimitMiddleware
from app.infrastructure.cache.redis import ping_redis
from app.infrastructure.database.session import engine
from app.lifespan import lifespan
from app.modules.auth.router import router as auth_router
from app.modules.chat.router import router as chat_router
from app.modules.citations.router import router as citations_router
from app.modules.conversations.router import router as conversations_router
from app.modules.documents.router import router as documents_router
from app.modules.voice.router import router as voice_router
from app.modules.workspaces.router import router as workspaces_router

settings = get_settings()
configure_logging(settings.log_level)
logger = logging.getLogger(__name__)

api = APIRouter(prefix="/api/v1")
api.include_router(auth_router)
api.include_router(workspaces_router)
api.include_router(documents_router)
api.include_router(chat_router)
api.include_router(citations_router)
api.include_router(conversations_router)
api.include_router(voice_router)


@api.get("/health/live", tags=["health"])
def live() -> dict[str, str]:
    return {"status": "ok"}


@api.get("/health/ready", tags=["health"])
async def ready() -> JSONResponse:
    checks: dict[str, bool] = {"postgres": False, "redis": await ping_redis(settings.redis_url)}
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        checks["postgres"] = True
    except Exception:
        logger.warning("postgres_not_ready")
    status_code = 200 if all(checks.values()) else 503
    return JSONResponse(
        {"status": "ok" if status_code == 200 else "degraded", "checks": checks},
        status_code=status_code,
    )


def create_application() -> FastAPI:
    application = FastAPI(
        title="PustakTalk API",
        version="0.1.0",
        description="Page-aware, locally hosted document intelligence.",
        lifespan=lifespan,
    )
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["GET", "POST", "DELETE"],
        allow_headers=["Content-Type", "X-Request-ID"],
    )
    application.add_middleware(SecurityHeadersMiddleware)
    application.add_middleware(RequestContextMiddleware)
    application.add_middleware(RedisRateLimitMiddleware, settings=settings)

    @application.exception_handler(DomainError)
    async def domain_error_handler(_: Request, error: DomainError) -> JSONResponse:
        return JSONResponse(
            status_code=error.status_code,
            content={"error": {"code": error.code, "message": error.detail}},
        )

    application.include_router(api)
    return application


app = create_application()
