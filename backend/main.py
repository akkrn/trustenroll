import logging
import os

import aioredis
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from logging_config import setup_logging
from middleware import log_ip_middleware
from tortoise.contrib.fastapi import register_tortoise

from api_routes import api_router

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_URL = (
    os.getenv("DATABASE_URL")
    or f"postgres://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

load_dotenv()
logger = logging.getLogger(__name__)
setup_logging()


def create_app():
    app = FastAPI()

    app.middleware("http")(log_ip_middleware)

    @app.on_event("startup")
    async def startup_event():
        redis = aioredis.from_url(
            REDIS_URL,
            decode_responses=False,
            encoding="utf8",
        )
        FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

    app.include_router(api_router)

    register_tortoise(
        app,
        db_url=DB_URL,
        modules={"models": ["models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", reload=False)
