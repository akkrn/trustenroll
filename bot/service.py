from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from models import BotUser, Card, MainCategory, SubCategory


async def is_authorized(user_id):
    return await BotUser.exists(telegram_id=user_id)


async def register_user(user_id, username, fullname):
    exists = await BotUser.exists(telegram_id=user_id)
    if not exists:
        await BotUser.create(
            telegram_id=user_id, username=username, name=fullname
        )
        return True
    return False


async def get_main_category_buttons():
    categories = await MainCategory.all()
    buttons = [
        InlineKeyboardButton(text=cat.name, callback_data=f"main_{cat.id}")
        for cat in categories
    ]
    return InlineKeyboardMarkup(inline_keyboard=[buttons])


async def get_subcategory_buttons(main_category_id):
    subcategories = await SubCategory.filter(main_category_id=main_category_id)
    buttons = [
        InlineKeyboardButton(text=sub.name, callback_data=f"sub_{sub.id}")
        for sub in subcategories
    ]
    return InlineKeyboardMarkup(inline_keyboard=[buttons])


async def parse_and_save_cards(text, subcategory_id):
    entries = text.strip().split("\n\n")
    for entry in entries:
        lines = entry.strip().split("\n")
        bank_name = lines[0].strip()
        for line in lines[1:]:
            card_info = line.strip()
            await Card.create(
                bank_name=bank_name,
                card_name=card_info,
                subcategory_id=subcategory_id,
            )
