from asyncio import run
from aiogram import Bot, Dispatcher

from config_reader import config
from handlers import common, game, help, catalog, contact, answer
from utils.comands import set_commands

from db import init_db


async def main():
    bot = Bot(token=config.bot_token.get_secret_value())

    await set_commands(bot)

    dp = Dispatcher()

    dp.include_routers(
        common.router,
        contact.router,
        help.router,
        catalog.router,
        game.router,
        answer.router
    )

    init_db()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    run(main())
