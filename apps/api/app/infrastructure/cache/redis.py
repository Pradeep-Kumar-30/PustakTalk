from arq.connections import RedisSettings, create_pool


async def ping_redis(url: str) -> bool:
    try:
        client = await create_pool(RedisSettings.from_dsn(url))
        try:
            return bool(await client.ping())
        finally:
            await client.aclose()
    except Exception:
        return False
