from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from keyboards.common_kb import menu

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        text='''Добро пожаловать в демонстрационный бот.'''
    )
    await message.answer(
        text='Здесь представлены основные функции, которые вы можете использовать в своем телеграм боте.'
    )
    await message.answer(
        text='Так как это демострационый бот, здесь не представлено некоторые функции (рассылка, администрирование, добовление контанта и т.д.)'
    )
    await message.answer(
        text='За подробной информации о доступных возможностях, обращайтесь к разработчику\n/contact'
    )

