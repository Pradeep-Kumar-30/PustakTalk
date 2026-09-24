import logging
import time

from arq.connections import RedisSettings, create_pool
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import Settings

logger = logging.getLogger(__name__)


class RedisRateLimitMiddleware(BaseHTTPMiddleware):
    """A fixed-window limiter; Redis outages are logged and fail open to preserve availability."""

    def __init__(self, app, settings: Settings) -> None:  # type: ignore[no-untyped-def]
        super().__init__(app)
        self._settings = settings

    async def dispatch(self, request, call_next):  # type: ignore[no-untyped-def]
        if request.url.path.endswith("/health/live") or request.url.path.endswith("/health/ready"):
            return await call_next(request)
        client_ip = request.client.host if request.client else "unknown"
        window = int(time.time() // 60)
        try:
            redis = await create_pool(RedisSettings.from_dsn(self._settings.redis_url))
            try:
                key = f"rate:{client_ip}:{window}"
                attempts = await redis.incr(key)
                if attempts == 1:
                    await redis.expire(key, 61)
            finally:
                await redis.aclose()
            if attempts > self._settings.rate_limit_per_minute:
                return JSONResponse(
                    {
                        "error": {
                            "code": "rate_limited",
                            "message": "Too many requests. Please try again shortly.",
                        }
                    },
                    status_code=429,
                )
        except Exception as error:
            logger.warning("rate_limit_unavailable", extra={"error_type": type(error).__name__})
        return await call_next(request)
