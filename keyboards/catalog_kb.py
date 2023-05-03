from typing import Optional

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class CatalogAction(CallbackData, prefix="help"):
    action: str
    remove: Optional[bool]


def catalog() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text='Виды сообщений',
        callback_data=CatalogAction(action='types')
    )
    # kb.button(
    #     text='Добавить',
    #     callback_data=CatalogAction(action='add')
    # )
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def message_types() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text='Текст',
        callback_data=CatalogAction(action='text')
    )
    kb.button(
        text='Фото',
        callback_data=CatalogAction(action='photo')
    )
    kb.button(
        text='Видео',
        callback_data=CatalogAction(action='video')
    )
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def back_message_types(remove: bool = False) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text='Назад',
        callback_data=CatalogAction(action='types', remove=remove)
    )
    return kb.as_markup(resize_keyboard=True)
