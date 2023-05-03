import datetime

from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from keyboards.help_kb import HelpAction, question, agree
from db import add_message

router = Router()


class SendMessage(StatesGroup):
    question = State()
    choosing_food_size = State()


@router.message(Command("help"))
async def cmd_help(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text='Здесь вы можете задать свой вопрос',
        reply_markup=question()
    )


@router.callback_query(HelpAction.filter(F.action == 'question'))
async def write_question(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text='Напишите свой вопрос'
    )
    await state.set_state(SendMessage.question)


@router.message(SendMessage.question)
async def agree_question(message: Message, state: FSMContext):
    await state.update_data(
        message_id=message.message_id,
        message_text=message.text,
        user_id=message.from_user.id, )
    await message.reply(
        text='Отправить вопрос?',
        reply_markup=agree()
    )


@router.callback_query(HelpAction.filter(F.action == 'cancel'))
async def cancel(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text='Отправка отменена'
    )
    await state.clear()


@router.callback_query(HelpAction.filter(F.action == 'send'))
async def send_question(callback: CallbackQuery, state: FSMContext, bot: Bot):
    question_data = await state.get_data()
    add_message(
        message_id=question_data['message_id'],
        message_text=question_data['message_text'],
        send_date=datetime.datetime.now(),
        user_id=callback.from_user.id
    )
    await bot.send_message(
        chat_id=398292556,
        text='Пришел новый вопрос!'
    )
    await callback.message.delete()
    await callback.message.answer(
        text='Сообщение отправлено. Скоро вам ответят'
    )
    await callback.answer()
    await state.clear()


