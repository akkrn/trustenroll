import os
from aiocache import caches
from dotenv import load_dotenv

load_dotenv()

GLOBAL_TTL: int = 600


async def set_cache_config():
    caches.set_config(
        {
            "default": {
                "cache": "aiocache.RedisCache",
                "endpoint": os.getenv("REDIS_HOST"),
                "port": int(os.getenv("REDIS_PORT")),
                "timeout": 1,
                "serializer": {"class": "aiocache.serializers.JsonSerializer"},
            }
        }
    )
