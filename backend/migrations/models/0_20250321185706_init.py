from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "admin" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(50) NOT NULL UNIQUE,
    "password" VARCHAR(200) NOT NULL
);
CREATE TABLE IF NOT EXISTS "maincategory" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS "subcategory" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "main_category_id" INT NOT NULL REFERENCES "maincategory" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "card" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "bank_name" VARCHAR(255) NOT NULL,
    "card_name" TEXT NOT NULL,
    "subcategory_id" INT NOT NULL REFERENCES "subcategory" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
