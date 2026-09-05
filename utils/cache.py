from core.redis import redis_client


async def key(namespace: str, suffix: str) -> str:
    """Build a cache key stamped with the namespace's current version."""
    version = await redis_client.get(f"cache_version:{namespace}")
    return f"{namespace}:v{int(version or 0)}:{suffix}"

async def invalidate(namespace: str) -> None:
    """Retire every cached key of one resource, e.g. invalidate("order").

    Nothing is scanned or deleted: bumping the version makes keys built before
    it unreachable, and they die on their own TTL. Scanning the whole database
    on every write was O(all keys) and blocked Redis for everyone else.
    """
    await redis_client.incr(f"cache_version:{namespace}")