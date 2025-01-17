from aiogram.types import (
    Message,
    ReplyKeyboardRemove,
    CallbackQuery,
    # CallbackQuery,
    # InlineKeyboardMarkup,
    # InlineKeyboardButton,
)
from fluent.runtime import FluentLocalization

from datetime import datetime


# async def send_localized_message(
#     message: Message,
#     l10n: FluentLocalization,
#     text_key: str,
#     reply_markup=ReplyKeyboardRemove(),
# ):
#     """
#     Utility function to send a localized message.
#     """
#     localized_text = l10n.format_value(text_key)
#     await message.answer(localized_text, reply_markup=reply_markup)
async def send_localized_message(
    message_or_callback: Message | CallbackQuery,
    l10n: FluentLocalization,
    text_key: str,
    reply_markup=ReplyKeyboardRemove(),
):
    """
    Utility function to send a localized message.
    Can handle both Message and CallbackQuery.
    """
    localized_text = l10n.format_value(text_key)

    # Проверяем тип входящего объекта
    if isinstance(message_or_callback, CallbackQuery):
        # Ответ на CallbackQuery
        await message_or_callback.message.answer(
            localized_text, reply_markup=reply_markup
        )
        # Закрываем всплывающее уведомление
        await message_or_callback.answer()
    elif isinstance(message_or_callback, Message):
        # Ответ на Message
        await message_or_callback.answer(localized_text, reply_markup=reply_markup)


# async def send_localized_callback_message(
#     message: Message,
#     l10n: FluentLocalization,
#     text_key: str,
#     buttons: list[tuple[str, str]],
# ):
#     """
#     Utility function to send a localized message with an inline keyboard.
#
#     Args:
#         message (Message): Telegram message object.
#         l10n (FluentLocalization): Localization object.
#         text_key (str): Localization key for the message text.
#         buttons (list[tuple[str, str]]): List of button texts and their callback data.
#     """
#     localized_text = l10n.format_value(text_key)
#     keyboard = InlineKeyboardMarkup(row_width=2)
#
#     # Add buttons to the inline keyboard
#     for button_text_key, callback_data in buttons:
#         button_text = l10n.format_value(button_text_key)
#         keyboard.add(
#             InlineKeyboardButton(text=button_text, callback_data=callback_data)
#         )
#
#     # Send the message with the inline keyboard
#     await message.answer(localized_text, reply_markup=keyboard)


async def get_current_datetime():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M")
