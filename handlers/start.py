from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluent.runtime import FluentLocalization

import keyboards.keyboards as kb
from database.requests import get_user_by_tg_id, add_user_to_db

start_router = Router()


async def send_localized_message(
    message: Message, l10n: FluentLocalization, text_key: str, reply_markup=None
):
    """
    Utility function to send a localized message.
    """
    localized_text = l10n.format_value(text_key)
    await message.answer(localized_text, reply_markup=reply_markup)


@start_router.message(CommandStart())
async def start_command(message: Message, state: FSMContext, l10n: FluentLocalization):
    """
    Command handler /start.
    """
    if message.chat.type == "private":
        await state.clear()
        user_tg_id = message.from_user.id
        user_name = message.from_user.username
        user_full_name = message.from_user.full_name
        language_code = message.from_user.language_code or "ru"

        # Проверяем пользователя в БД
        user = await get_user_by_tg_id(user_tg_id)

        if not user:
            await add_user_to_db(user_tg_id, user_name, user_full_name, language_code)

        await send_localized_message(
            message,
            l10n,
            "welcome-text",
            reply_markup=await kb.start_menu(l10n),
        )


@start_router.message(F.text.in_({"⁉️ Поддержка", "⁉️ Support"}))
async def start_support(message: Message, l10n: FluentLocalization):
    """
    Handler for the "Support" button.
    """
    await send_localized_message(
        message,
        l10n,
        "support",
        reply_markup=await kb.back_to_menu(l10n),
    )


@start_router.message(F.text.in_({"👥 Пригласить друзей", "👥 Invite friends"}))
async def invite_friends(message: Message, l10n: FluentLocalization):
    """
    Handler for the "Invite friends" button.
    """
    await send_localized_message(
        message,
        l10n,
        "invite",
        reply_markup=await kb.back_to_menu(l10n),
    )


@start_router.message(F.text.in_({"↩️ Назад в главное меню", "↩️ Back to main menu"}))
async def back_to_main_menu(
    message: Message, state: FSMContext, l10n: FluentLocalization
):
    """
    Handler for returning to the main menu.
    """
    await send_localized_message(
        message,
        l10n,
        "welcome-text",
        reply_markup=await kb.start_menu(l10n),
    )
    await state.clear()
