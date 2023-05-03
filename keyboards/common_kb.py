from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def menu() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='/help')
    kb.button(text='/contact')

    kb.button(text='/catalog')
    kb.button(text='/admin')
    kb.button(text='/game')
    return kb.as_markup(resize_keyboard=True)
