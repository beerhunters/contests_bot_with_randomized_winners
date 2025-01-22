import re

from aiogram.enums import ParseMode
from aiogram.types import (
    Message,
    ReplyKeyboardRemove,
    CallbackQuery,
)
from fluent.runtime import FluentLocalization

from datetime import datetime


# async def send_localized_message(
#     message_or_callback: Message | CallbackQuery,
#     l10n: FluentLocalization,
#     text_key: str,
#     reply_markup=ReplyKeyboardRemove(),
#     show_alert: bool = False,
# ):
#     """
#     Utility function to send a localized message.
#     Can handle both Message and CallbackQuery.
#     """
#     localized_text = l10n.format_value(text_key)
#
#     # Проверяем тип входящего объекта
#     if isinstance(message_or_callback, CallbackQuery):
#         # Ответ на CallbackQuery
#         await message_or_callback.message.answer(
#             localized_text, reply_markup=reply_markup, show_alert=show_alert
#         )
#         # Закрываем всплывающее уведомление
#         await message_or_callback.answer()
#     elif isinstance(message_or_callback, Message):
#         # Ответ на Message
#         await message_or_callback.answer(localized_text, reply_markup=reply_markup)


async def send_localized_message(
    message_or_callback: Message | CallbackQuery,
    l10n: FluentLocalization,
    text_key: str,
    reply_markup=ReplyKeyboardRemove(),
    show_alert: bool = False,
    prefix: str = "",  # Новый параметр для текста в начале сообщения
    postfix: str = "",  # Новый параметр для текста в начале сообщения
):
    """
    Utility function to send a localized message with an optional prefix.
    Can handle both Message and CallbackQuery.
    """
    # Формируем локализованный текст
    localized_text = l10n.format_value(text_key)
    full_message = f"{prefix}\n\n{localized_text}\n\n{postfix}"

    # Проверяем тип входящего объекта
    if isinstance(message_or_callback, CallbackQuery):
        # Ответ на CallbackQuery
        await message_or_callback.message.answer(
            full_message,
            reply_markup=reply_markup,
            show_alert=show_alert,
        )
        # Закрываем всплывающее уведомление
        await message_or_callback.answer()
    elif isinstance(message_or_callback, Message):
        # Ответ на Message
        await message_or_callback.answer(full_message, reply_markup=reply_markup)


async def get_current_datetime():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M")


# def escape_markdown_v2(text: str) -> str:
#     """Экранирует зарезервированные символы MarkdownV2."""
#     return re.sub(r"([!#()*+\-.?[\\]^_`{|}~])", r"\\\1", text)


# def escape_markdown_v2(text: str) -> str:
#     """Экранирует специальные символы для MarkdownV2."""
#     # Перечень символов, которые нужно экранировать
#     special_chars = r"_*[]()~`>#+-=|{}.!"
#     escape_pattern = re.compile(f"([{re.escape(special_chars)}])")
#     return escape_pattern.sub(r"\\\1", text)
