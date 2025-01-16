from aiogram.types import Message, ReplyKeyboardRemove
from fluent.runtime import FluentLocalization


async def send_localized_message(
    message: Message,
    l10n: FluentLocalization,
    text_key: str,
    reply_markup=ReplyKeyboardRemove(),
):
    """
    Utility function to send a localized message.
    """
    localized_text = l10n.format_value(text_key)
    await message.answer(localized_text, reply_markup=reply_markup)
