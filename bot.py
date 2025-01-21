import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from dotenv import load_dotenv

from handlers.contest import contest_router

from handlers.contest_for_users import contest_for_users
from handlers.my_contest import my_contest_router
from handlers.start import start_router

from middlewares.localization import L10nMiddleware

from tools.logger import logger
from tools.scheduler import scheduler


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
    dp.include_routers(
        start_router,
        contest_router,
        my_contest_router,
        contest_for_users,
    )

    # Commands registration
    bot_commands = [BotCommand(command="/start", description="Запустить бота")]
    await bot.set_my_commands(bot_commands)

    # Запускаем планировщик в контексте `asyncio`
    scheduler.start()

    # Starting the bot
    try:
        logger.info("Бот запущен и работает...")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Ошибка при работе бота: {e}")
    finally:
        scheduler.shutdown()  # Останавливаем планировщик перед завершением работы бота
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
