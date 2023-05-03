from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.utils.chat_action import ChatActionSender

from keyboards.catalog_kb import CatalogAction, catalog, message_types, back_message_types

router = Router()


@router.message(Command("catalog"))
async def cmd_catalog(message: Message, state: FSMContext):
    """Показ каталога"""

    await state.clear()
    await message.answer(
        text='''Здесь вы можете ознакомиться с принципом работы каталогов''',
        reply_markup=message_types()
    )


@router.callback_query(CatalogAction.filter(F.action == 'types'))
async def cancel_send(callback: CallbackQuery, callback_data: CatalogAction, bot: Bot):
    if callback_data.remove:
        await callback.message.delete()
        await bot.send_message(
            chat_id=callback.from_user.id,
            text='Бот может показывать различные виды сообщений',
            reply_markup=message_types()
        )
    else:
        await callback.message.edit_text(
            text='Бот может показывать различные виды сообщений',
            reply_markup=message_types()

        )
    await callback.answer()


@router.callback_query(CatalogAction.filter(F.action == 'text'))
async def send_text(callback: CallbackQuery):
    """Отправка текста"""

    await callback.message.edit_text(
        text='Это обычное текстовое сообщение. \nВ него может добавлена ссылка и <b>отформатированный текст</b>\nhttps://www.youtube.com/watch?v=-452p_9ESbM',
        parse_mode='HTML',
        reply_markup=back_message_types(remove=False)
    )
    await callback.answer()


@router.callback_query(CatalogAction.filter(F.action == 'photo'))
async def send_photo(callback: CallbackQuery, bot: Bot):
    """Отправка фото"""

    async with ChatActionSender.upload_photo(chat_id=callback.from_user.id):
        await callback.message.delete()
        await bot.send_photo(
            chat_id=callback.from_user.id,
            photo=FSInputFile('file/cat.jpeg'),
            caption='Можно отправлять фото с описанием',
            reply_markup=back_message_types(remove=True)
        )
    await callback.answer()


@router.callback_query(CatalogAction.filter(F.action == 'video'))
async def send_video(callback: CallbackQuery, bot: Bot):
    """Отправка видео"""

    async with ChatActionSender.upload_video(chat_id=callback.from_user.id):
        await callback.message.delete()
        await bot.send_video(
            chat_id=callback.from_user.id,
            video=FSInputFile('file/cat.mp4'),
            caption='Можно отправлять видео с описанием',
            reply_markup=back_message_types(remove=True)
        )
    await callback.answer()
