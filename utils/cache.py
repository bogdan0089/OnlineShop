from core.redis import redis_client


async def invalidate(prefix: str) -> None:
    """Drop every cached key of one resource, e.g. invalidate("order")."""
    async for key in redis_client.scan_iter(f"{prefix}*"):
        await redis_client.unlink(key)
