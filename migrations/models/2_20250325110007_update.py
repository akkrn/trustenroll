from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "botuser" ADD "username" VARCHAR(255);
        ALTER TABLE "botuser" ADD "name" VARCHAR(255);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "botuser" DROP COLUMN "username";
        ALTER TABLE "botuser" DROP COLUMN "name";"""
