import os

import aioredis
import uvicorn
from admin import configure_admin
from dotenv import load_dotenv
from exception import register_exception_handlers
from fastapi import FastAPI
from fastapi_admin.app import app as admin_app
from routes import router as redirect_router
from tortoise.contrib.fastapi import register_tortoise

load_dotenv()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
TEMPLATE_FOLDER = os.path.join(BASE_DIR, "templates")
DB_URL = (
    os.getenv("DATABASE_URL")
    or f"postgres://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)


def create_app():
    app = FastAPI()

    @app.on_event("startup")
    async def startup_event():
        redis = await aioredis.from_url(REDIS_URL, decode_responses=False)
        await configure_admin(admin_app, redis, TEMPLATE_FOLDER)
        await register_exception_handlers(admin_app)

    app.include_router(redirect_router)
    app.mount("/admin", admin_app)
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
    uvicorn.run(app, host="0.0.0.0", port=1142)
