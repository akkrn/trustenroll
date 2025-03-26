import asyncio
import os

from aiogram import Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from service import get_main_category_buttons, get_subcategory_buttons, is_authorized, parse_and_save_cards, register_user, show_main_menu
from states import UploadStates
from models import Card

router = Router()
load_dotenv()

secret_command = os.getenv("SECRET_COMMAND")


@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    if not await is_authorized(message.from_user.id):
        await message.answer("Access denied.")
        return
    await show_main_menu(message, state, False)


@router.callback_query(lambda c: c.data == "action_delete")
async def start_deletion(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(UploadStates.waiting_for_delete_input)
    await callback.message.edit_text("Send card lines to delete")


@router.message(UploadStates.waiting_for_delete_input)
async def delete_cards_handler(message: types.Message, state: FSMContext):
    if not await is_authorized(message.from_user.id):
        await message.answer("Access denied.", show_alert=True)
        return
    lines = message.text.strip().split("\n")
    not_found = []
    deleted_count = 0

    for line in lines:
        number = line.strip().split("|")[0].strip().lstrip("#")
        if len(number) == 4:
            deleted = await Card.filter(card_name__startswith=f"#{number}").delete()
        if deleted == 0:
            not_found.append(line)
        else:
            deleted_count += deleted

    if not_found:
        text = "⚠️ Not found:\n" + "\n".join(not_found)
    else:
        text = f"✅ {deleted_count} card(s) deleted."
    text += "\n\n Delete more?"
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⬅️ Back to menu", callback_data="back_to_menu")]])
    await message.answer(text, reply_markup=kb)


@router.callback_query(lambda c: c.data == "back_to_menu")
async def handle_back(callback_query: types.CallbackQuery, state: FSMContext):
    if not await is_authorized(callback_query.from_user.id):
        await callback_query.answer("Access denied.", show_alert=True)
        return
    await show_main_menu(callback_query.message, state)


@router.message(Command(secret_command))
async def access(message: types.Message):
    registered = await register_user(
        message.from_user.id,
        message.from_user.username,
        f"{message.from_user.first_name} {message.from_user.last_name}",
    )
    if registered:
        await message.answer("Access granted. You can now use the bot.")
    else:
        await message.answer("You already have access.")


@router.callback_query(lambda c: c.data.startswith("action_add"))
async def add_card_handler(callback_query: types.CallbackQuery, state: FSMContext):
    if not await is_authorized(callback_query.from_user.id):
        await callback_query.answer("Access denied.", show_alert=True)
        return
    kb = await get_main_category_buttons()
    await callback_query.message.edit_text("Select a main category:", reply_markup=kb)
    await state.set_state(UploadStates.waiting_for_main_category)


@router.callback_query(lambda c: c.data.startswith("main_"))
async def main_category_handler(callback_query: types.CallbackQuery, state: FSMContext):
    if not await is_authorized(callback_query.from_user.id):
        await callback_query.answer("Access denied.", show_alert=True)
        return

    category_id = int(callback_query.data.split("_")[1])
    await state.update_data(main_category_id=category_id)

    kb = await get_subcategory_buttons(category_id)
    await callback_query.message.edit_text("Select a subcategory:", reply_markup=kb)
    await state.set_state(UploadStates.waiting_for_subcategory)


@router.callback_query(lambda c: c.data.startswith("sub_"))
async def subcategory_handler(callback_query: types.CallbackQuery, state: FSMContext):
    if not await is_authorized(callback_query.from_user.id):
        await callback_query.answer("Access denied.", show_alert=True)
        return

    subcategory_id = int(callback_query.data.split("_")[1])
    await state.update_data(subcategory_id=subcategory_id)

    await callback_query.message.edit_text("Now send me the cards info in the required format.")
    await state.set_state(UploadStates.waiting_for_cards_text)


@router.message(~StateFilter(UploadStates.waiting_for_cards_text))
async def catch_unexpected_messages(message: types.Message, state: FSMContext):
    reminder = await message.answer("Please select a category first.")
    await asyncio.sleep(1)
    try:
        await message.delete()
        await reminder.delete()
    except Exception:
        pass


@router.message(UploadStates.waiting_for_cards_text)
async def process_cards_text(message: types.Message, state: FSMContext):
    if not await is_authorized(message.from_user.id):
        await message.answer("Access denied.")
        return

    data = await state.get_data()
    subcategory_id = data.get("subcategory_id")

    text = message.text.strip()
    if not text:
        await message.answer("Message is empty. Send again.")
        return

    await parse_and_save_cards(text, subcategory_id)

    await message.answer("Cards saved. Choose a main category again.")
    kb = await get_main_category_buttons()

    await message.answer("Select a main category:", reply_markup=kb)
    await state.set_state(UploadStates.waiting_for_main_category)
