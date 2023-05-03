from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='catalog',
            description='Открыть каталог'
        ),
        BotCommand(
            command='help',
            description='Задать вопрос'
        ),
        BotCommand(
            command='game',
            description='Играть'
        ),
        BotCommand(
            command='contact',
            description='Получить контакты разработчика'
        )
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())
