import os
from redis.asyncio import Redis, ConnectionPool

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
pool = ConnectionPool.from_url(REDIS_URL, decode_responses=True)

async def get_redis() -> Redis:
    return Redis(connection_pool=pool)

async def get_user_from_cache(user_name: str) -> dict | None:
    r = await get_redis()
    name_key = f"user:{user_name}"
    data = await r.get(name_key)
    if data:
        import json
        return json.loads(data)
    return None

async def set_user_to_cache(user_name: str, user_data, ttl: int = 60):
    r = await get_redis()
    key_name = f"user:{user_name}"
    import json
    await r.setex(key_name, ttl, json.dumps(user_data))

async def delete_user_from_cache(user_name: str):
    r = await get_redis()
    key_name = f"user:{user_name}"
    await r.delete(key_name)