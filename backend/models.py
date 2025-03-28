import os

from dotenv import load_dotenv
from fastapi_admin.models import AbstractAdmin
from tortoise import fields, models

load_dotenv()


class MainCategory(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    main_category = fields.ForeignKeyField("models.MainCategory", related_name="subcategories")

    def __str__(self):
        return self.name


class Card(models.Model):
    id = fields.IntField(pk=True)
    bank_name = fields.CharField(max_length=255)
    card_name = fields.TextField()
    subcategory = fields.ForeignKeyField("models.SubCategory", related_name="cards")

    def __str__(self):
        return self.card_name


class Admin(AbstractAdmin):
    pass


class BotUser(models.Model):
    id = fields.IntField(pk=True)
    telegram_id = fields.BigIntField(unique=True)
    username = fields.CharField(max_length=255, null=True)
    name = fields.CharField(max_length=255, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)


class VisitLog(models.Model):
    id = fields.IntField(pk=True)
    ip = fields.CharField(max_length=45)
    timestamp = fields.DatetimeField(auto_now_add=True)
    device = fields.CharField(max_length=128, null=True)
    os = fields.CharField(max_length=128, null=True)
    browser = fields.CharField(max_length=128, null=True)


TORTOISE_ORM = {
    "connections": {"default": os.getenv("DATABASE_URL")},
    "apps": {
        "models": {
            "models": ["backend.models", "aerich.models"],
            "default_connection": "default",
        }
    },
}
