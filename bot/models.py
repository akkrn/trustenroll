from tortoise import fields, models


class BotUser(models.Model):
    telegram_id = fields.BigIntField(unique=True)
    username = fields.CharField(max_length=255, null=True)
    name = fields.CharField(max_length=255, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)


class MainCategory(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)


class SubCategory(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    main_category = fields.ForeignKeyField("models.MainCategory", related_name="subcategories")


class Card(models.Model):
    id = fields.IntField(pk=True)
    bank_name = fields.CharField(max_length=255)
    card_name = fields.TextField()
    subcategory = fields.ForeignKeyField("models.SubCategory", related_name="cards")


class VisitLog(models.Model):
    id = fields.IntField(pk=True)
    ip = fields.CharField(max_length=45)
    timestamp = fields.DatetimeField(auto_now_add=True)
    device = fields.CharField(max_length=128, null=True)
    os = fields.CharField(max_length=128, null=True)
    browser = fields.CharField(max_length=128, null=True)
