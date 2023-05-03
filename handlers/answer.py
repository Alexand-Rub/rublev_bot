import datetime

from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from middlewares.admin_check import AdminBarrierCallback, AdminBarrierMassage
from keyboards.answer_kb import AnswerAction, users, question_list, question_action, agree_send
from db import get_user_question, get_question, remove_question, get_users

router = Router()
router.message.middleware(AdminBarrierMassage())
router.callback_query.middleware(AdminBarrierCallback())


class SendAnswer(StatesGroup):
    answer = State()


@router.message(Command("answer"))
async def cmd_answer(message: Message, state: FSMContext):
    """Показывает список пользователь задавших вопрос"""

    await state.clear()

    if len(get_users()) > 0:
        await message.answer(
            text='Актуальные вопросы',
            reply_markup=users()
        )
    else:
        await message.answer(text='Вопросов нет')


@router.callback_query(AnswerAction.filter(F.action == 'user'))
async def choose_question(callback: CallbackQuery, callback_data: AnswerAction):
    """Показывает список вопросов пользователя"""

    text = 'Вопросы пользователя'
    questions = get_user_question(callback_data.user_id)
    question_dict = {}
    for question in questions:
        text += '\n\n<u>{date}</u>\n{text}'.format(
            date=question[2],
            text=question[1]
        )
        question_dict[question[2]] = question[0]

    await callback.message.edit_text(
        text=text,
        parse_mode='HTML',
        reply_markup=question_list(question_dict)
    )


@router.callback_query(AnswerAction.filter(F.action == 'question_action'))
async def answer_question(callback: CallbackQuery, callback_data: AnswerAction, state: FSMContext):
    """Показывает действия с вопросом"""

    await state.update_data(message_id=callback_data.message_id)
    await callback.message.answer(
        text='Выберете действие',
        reply_markup=question_action()
    )


@router.callback_query(AnswerAction.filter(F.action == 'delete'))
async def delete_question(callback: CallbackQuery, state: FSMContext):
    """Удаление вопроса"""

    answer_data = await state.get_data()
    remove_question(massage_id=answer_data['message_id'])
    await callback.message.edit_text(text='Вопрос удален')
    await callback.answer()


@router.callback_query(AnswerAction.filter(F.action == 'answer'))
async def delete_question(callback: CallbackQuery, callback_data: AnswerAction, state: FSMContext):
    """Написание ответа"""

    await callback.message.edit_text(text='Напишите ответ')
    await callback.answer()
    await state.set_state(SendAnswer.answer)


@router.message(SendAnswer.answer)
async def agree_answer(message: Message, state: FSMContext):
    """Подтверждение ответа"""

    answer_data = await state.get_data()
    question = get_question(answer_data['message_id'])
    text = 'На ваш вопрос ответили\n\n<b>Дата:</b> {send_date}\n\n<b>Вопрос:</b> {massage_text}\n\n<b>Ответ:</b> {answer}'.format(
        send_date=question[2].split('.')[0],
        massage_text=question[1],
        answer=message.text
    )
    await state.update_data(
        answer=text,
        user_id=question[3])
    await message.answer(
        text=text,
        parse_mode='HTML',
        reply_markup=agree_send()
    )


@router.callback_query(AnswerAction.filter(F.action == 'cancel'))
async def cancel_answer(callback: CallbackQuery, state: FSMContext):
    """Отмена отправки ответа"""

    await callback.message.edit_text(text="Отправка отменена")
    await state.clear()


@router.callback_query(AnswerAction.filter(F.action == 'send'))
async def send_answer(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """Отправка ответа"""

    answer_data = await state.get_data()
    await bot.send_message(
        chat_id=answer_data['user_id'],
        text=answer_data['answer'],
        parse_mode='HTML'
    )
    await callback.message.edit_text(text='Ответ отправлен')
    remove_question(massage_id=answer_data['message_id'])
    print(answer_data['message_id'])


