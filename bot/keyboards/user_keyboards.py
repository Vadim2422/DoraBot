from aiogram.utils.keyboard import ReplyKeyboardBuilder
from bot.lexicon.lexicon_ru import LEXICON_RU

def get_set_admin_kb():
    builder = ReplyKeyboardBuilder()
    builder.button('/dora')
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

