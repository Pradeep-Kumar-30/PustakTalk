from uuid import UUID

from arq.connections import RedisSettings, create_pool

from app.core.config import Settings


async def enqueue_document_processing(document_id: UUID, settings: Settings) -> None:
    queue = await create_pool(RedisSettings.from_dsn(settings.redis_url))
    try:
        await queue.enqueue_job("process_document", str(document_id))
    finally:
        await queue.aclose()
