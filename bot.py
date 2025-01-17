import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from dotenv import load_dotenv

from database.models import init_db
from handlers.contest import contest_router
from handlers.start import start_router
from middlewares.localization import L10nMiddleware

from tools.logger import logger


async def main():
    """
    The main function to start the bot
    """
    # Инициализация базы данных
    # await init_db()

    load_dotenv()
    bot = Bot(
        token=os.getenv("TELEGRAM_TOKEN"),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()

    # Middleware registration
    dp.message.outer_middleware(L10nMiddleware(default_locale="ru"))
    dp.callback_query.outer_middleware(L10nMiddleware(default_locale="ru"))

    # Handler registration
    dp.include_routers(start_router, contest_router)

    # Commands registration
    bot_commands = [BotCommand(command="/start", description="Перезапустить бота")]
    await bot.set_my_commands(bot_commands)

    # Starting the bot
    try:
        logger.info("Бот запущен и работает...")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Ошибка при работе бота: {e}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
