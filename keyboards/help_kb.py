from typing import Optional

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class HelpAction(CallbackData, prefix="help"):
    action: str
    chat_id: Optional[int]


def question() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text='Задать вопрос',
        callback_data=HelpAction(action='question')
    )
    return kb.as_markup(resize_keyboard=True)


def agree() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text='Отправить',
        callback_data=HelpAction(action='send')
    )
    kb.button(
        text='Отменить',
        callback_data=HelpAction(action='cancel')
    )
    return kb.as_markup(resize_keyboard=True)
