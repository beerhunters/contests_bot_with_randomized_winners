import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from dotenv import load_dotenv

from handlers.start import start_router
from logger import logger


async def main():
    """
    The main function to start the bot
    """

    load_dotenv()
    bot = Bot(
        token=os.getenv("TELEGRAM_TOKEN"),
    )
    dp = Dispatcher()

    # Handler registration
    dp.include_router(start_router)

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
