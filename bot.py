import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from dotenv import load_dotenv


# from handlers import user
from logger import logger
# from loguru import logger


async def main():
    """Главная функция для запуска бота."""
    load_dotenv()
    bot = Bot(
        token=os.getenv("TELEGRAM_TOKEN"),
    )
    dp = Dispatcher()

    # Регистрация обработчиков
    # dp.include_router(user)
    bot_commands = [BotCommand(command="/start", description="Перезапустить бота")]
    await bot.set_my_commands(bot_commands)

    # Запуск бота
    try:
        logger.info("Бот запущен...")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Ошибка при работе бота: {e}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
