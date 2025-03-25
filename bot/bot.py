import asyncio
import os
import logging

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from tortoise import Tortoise

from handlers import router
from logging_config import setup_logging

logger = logging.getLogger(__name__)

load_dotenv()
DB_URL = (
    os.getenv("DATABASE_URL")
    or f"postgres://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


async def init():
    await Tortoise.init(db_url=DB_URL, modules={"models": ["models"]})
    await Tortoise.generate_schemas()


async def main():
    setup_logging()
    logger.info("Bot is starting...")

    await init()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
