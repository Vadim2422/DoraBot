from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.lexicon.lexicon_ru import LEXICON_RU


def get_admin_ikb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=LEXICON_RU['cool'], callback_data='Cool')
    builder.button(text=LEXICON_RU['trash'], callback_data='Trash')
    builder.adjust(1)
    return builder.as_markup()
