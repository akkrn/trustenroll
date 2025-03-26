from aiogram.fsm.state import State, StatesGroup


class UploadStates(StatesGroup):
    waiting_for_main_category = State()
    waiting_for_subcategory = State()
    waiting_for_cards_text = State()
    waiting_for_delete_input = State()
