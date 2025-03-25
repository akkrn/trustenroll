from fastapi_admin.app import app as admin_app
from fastapi_admin.providers.login import UsernamePasswordProvider
from fastapi_admin.resources import Model
from fastapi_admin.widgets import filters

from models import Admin, BotUser, Card, MainCategory, SubCategory


async def configure_admin(redis, template_path):
    await admin_app.configure(
        redis=redis,
        template_folders=template_path,
        providers=[
            UsernamePasswordProvider(
                admin_model=Admin,
            ),
        ],
        # logo_url="https://www.flaticon.com/free-icon/user_10337203?term=admin&page=1&position=3&origin=tag&related_id=10337203",
    )
    await register_admin()


async def register_admin():
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
