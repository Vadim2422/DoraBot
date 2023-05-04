from aiogram.fsm.state import StatesGroup, State


class AddAdmin(StatesGroup):
    contact = State()
