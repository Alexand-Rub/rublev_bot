from typing import Optional, List, Dict

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db import get_users


class AnswerAction(CallbackData, prefix="answer"):
    action: str
    user_id: Optional[str]
    message_id: Optional[int]


def users() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    users_list = get_users()
    for i in range(len(users_list)):
        kb.button(
            text='Пользователь {num}'.format(num=i+1),
            callback_data=AnswerAction(
                action='user',
                user_id=users_list[i]
            )
        )
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def question_list(question_dict: Dict):
    kb = InlineKeyboardBuilder()
    for question_date in question_dict.keys():
        kb.button(
            text=question_date,
            callback_data=AnswerAction(
                action='question_action',
                message_id=question_dict[question_date]
            )
        )

    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def question_action():
    kb = InlineKeyboardBuilder()
    kb.button(
        text='Ответить',
        callback_data=AnswerAction(
            action='answer'
        )
    )
    kb.button(
        text='Удалить',
        callback_data=AnswerAction(
            action='delete'
        )
    )
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def agree_send():
    kb = InlineKeyboardBuilder()
    kb.button(
        text='Отправить',
        callback_data=AnswerAction(action='send')
    )
    kb.button(
        text='Отменить',
        callback_data=AnswerAction(action='cancel')
    )
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)
