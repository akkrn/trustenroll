import logging

from aiocache import cached
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from cache import GLOBAL_TTL
from models import BotUser, Card, MainCategory, SubCategory

logger = logging.getLogger(__name__)


@cached(ttl=GLOBAL_TTL)
async def is_authorized(user_id):
    logger.info(f"Calling DB for user_id={user_id}")
    return await BotUser.exists(telegram_id=user_id)


async def register_user(user_id, username, fullname):
    exists = await BotUser.exists(telegram_id=user_id)
    if not exists:
        await BotUser.create(telegram_id=user_id, username=username, name=fullname)
        return True
    return False


async def get_main_category_buttons():
    categories = await MainCategory.all()
    buttons = [[InlineKeyboardButton(text=cat.name, callback_data=f"main_{cat.id}")] for cat in categories]
    buttons.append([InlineKeyboardButton(text="⬅️ Back to menu", callback_data="back_to_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def get_subcategory_buttons(main_category_id):
    subcategories = await SubCategory.filter(main_category_id=main_category_id)
    buttons = [[InlineKeyboardButton(text=sub.name, callback_data=f"sub_{sub.id}")] for sub in subcategories]
    buttons.append([InlineKeyboardButton(text="⬅️ Back to menu", callback_data="back_to_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


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


async def show_main_menu(target, state: FSMContext, is_delete=True):
    await state.clear()
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="➕ Add cards", callback_data="action_add"),
                InlineKeyboardButton(text="❌ Delete cards", callback_data="action_delete"),
                InlineKeyboardButton(text="📊 Visits", callback_data="view_visits"),
            ]
        ]
    )
    await target.answer("Choose an action:", reply_markup=kb)
    if is_delete:
        await target.delete()
