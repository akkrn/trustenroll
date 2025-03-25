import asyncio
import os

from aiogram import Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv


from service import (
    get_main_category_buttons,
    get_subcategory_buttons,
    is_authorized,
    parse_and_save_cards,
    register_user,
)
from states import UploadStates

router = Router()
load_dotenv()

secret_command = os.getenv("SECRET_COMMAND")


@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    if not await is_authorized(message.from_user.id):
        await message.answer("Access denied.")
        return
    kb = await get_main_category_buttons()
    await message.answer("Select a main category:", reply_markup=kb)
    await state.set_state(UploadStates.waiting_for_main_category)


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
