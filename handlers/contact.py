from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message


router = Router()


@router.message(Command("contact"))
async def cmd_contact(message: Message, bot: Bot, state: FSMContext):
    await state.clear()
    await message.answer(
        text='Для получения подробной информации пишите ему'
    )
    await bot.send_contact(
        chat_id=message.from_user.id,
        first_name='Александр',
        last_name='Рублев',
        phone_number='79851985696'
    )
