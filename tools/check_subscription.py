from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest


async def check_subscription(user_id: int, channel_id: str, bot: Bot) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except TelegramBadRequest:
        # Например, если бот не администратор или пользователь не существует
        return False
