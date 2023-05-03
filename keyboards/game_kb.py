from typing import Optional, List

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class GameAction(CallbackData, prefix="game"):
    action: str
    letter: Optional[str]


def letters_kb(letters: List) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for letter in letters:
        kb.button(
            text=letter,
            callback_data=GameAction(action='letter', letter=letter)
        )
    kb.adjust(5)
    return kb.as_markup(resize_keyboard=True)


def restart():
    kb = InlineKeyboardBuilder()
    kb.button(
        text='Играть ещё',
        callback_data=GameAction(action='restart')
    )
    kb.adjust(5)
    return kb.as_markup(resize_keyboard=True)
