from fastapi_admin.providers.login import UsernamePasswordProvider
from fastapi_admin.resources import Model
from fastapi_admin.widgets import filters
from starlette.requests import Request
from tortoise.queryset import QuerySet

from models import Admin, BotUser, Card, MainCategory, SubCategory, VisitLog


async def configure_admin(admin_app, redis, template_path):
    await admin_app.configure(
        redis=redis,
        template_folders=[template_path],
        providers=[
            UsernamePasswordProvider(
                admin_model=Admin,
            ),
        ],
    )
    await register_admin(admin_app)


async def register_admin(admin_app):
    @admin_app.register
    class MainCategoryAdmin(Model):
        label = "Main Categories"
        model = MainCategory
        icon = "fa fa-folder"
        fields = [
            "id",
            "name",
        ]

    @admin_app.register
    class SubCategoryAdmin(Model):
        label = "Sub Categories"
        model = SubCategory
        icon = "fa fa-folder-open"
        fields = [
            "id",
            "name",
            "main_category",
        ]

    @admin_app.register
    class CardAdmin(Model):
        label = "Cards"
        model = Card
        icon = "fa fa-credit-card"
        fields = [
            "id",
            "bank_name",
            "card_name",
            "subcategory",
        ]
        filters = [
            filters.Search(
                name="card_name",
                label="Name",
                search_mode="contains",
                placeholder="Search for card name",
            ),
        ]

    @admin_app.register
    class BotUserAdmin(Model):
        label = "Bot Users"
        model = BotUser
        icon = "fa fa-folder"
        fields = ["id", "telegram_id", "username", "name", "created_at"]

    @admin_app.register
    class AdminAdmin(Model):
        label = "Admins"
        model = Admin
        icon = "fa fa-folder"
        fields = ["id", "username", "password"]

    @admin_app.register
    class VisitLogAdmin(Model):
        label = "Visit Logs"
        model = VisitLog
        fields = ["id", "ip", "device", "os", "browser", "timestamp"]
        filters = []

        @classmethod
        async def resolve_query_params(cls, request: Request, values: dict, qs: QuerySet):
            ret, qs = await super().resolve_query_params(request, values, qs)
            return ret, qs.order_by("-timestamp")
