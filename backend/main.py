import logging
import os

import aioredis
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from tortoise.contrib.fastapi import register_tortoise
from tortoise import Tortoise

from logging_config import setup_logging
from middleware import log_ip_middleware, RealIPMiddleware

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

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


# class RealIPMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):
#         # Проверяем X-Forwarded-For (список IP через запятую)
#         forwarded_for = request.headers.get("X-Forwarded-For")
#         if forwarded_for:
#             # Берём первый IP из списка (оригинальный клиент)
#             real_ip = forwarded_for.split(",")[0].strip()
#         else:
#             # Или используем X-Real-IP, если нет X-Forwarded-For
#             real_ip = request.headers.get("X-Real-IP", request.client.host)

#         # Устанавливаем IP в объект request.state для удобного доступа
#         request.state.real_ip = real_ip

#         response = await call_next(request)
#         return response


def create_app():
    app = FastAPI()
    app.add_middleware(RealIPMiddleware)

    app.middleware("http")(log_ip_middleware)

    @app.on_event("startup")
    async def startup_event():
        redis = aioredis.from_url(
            REDIS_URL,
            decode_responses=False,
            encoding="utf8",
        )
        FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
        await Tortoise.init(db_url=DB_URL, modules={"models": ["models"]})
        await Tortoise.generate_schemas()

    app.include_router(api_router)

    # register_tortoise(
    #     app,
    #     db_url=DB_URL,
    #     modules={"models": ["models"]},
    #     generate_schemas=True,
    #     add_exception_handlers=True,
    # )
    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", reload=False)
