from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
import keyboards.keyboards as kb
from logger import logger
from tools.tools import get_text

start_router = Router()


@start_router.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    """
    Command handler /start.
    """
    if message.chat.type == "private":
        await state.clear()
        user_tg_id = message.from_user.id
        user_name = message.from_user.username
        user_full_name = message.from_user.full_name

        # # Проверяем пользователя в БД
        # user = await get_user_by_tg_id(user_tg_id, db)
        #
        # if not user:
        #     # Добавляем нового пользователя
        #     await add_user_to_db(user_tg_id, user_name, user_full_name, language_code)
        # else:
        #     # Берем язык из БД
        #     language_code = user.language

        # Setting the default language
        language_code = message.from_user.language_code or "ru"

        print(user_tg_id, user_name, user_full_name, language_code)
        await state.update_data(language_code=language_code)

        welcome_text = await get_text(language_code, "WELCOME_TEXT")
        await message.answer(
            welcome_text, reply_markup=await kb.start_menu(language_code)
        )


@start_router.message(F.text.in_({"🌍 Change language", "🌍 Сменить язык"}))
async def prompt_language_change(message: Message, state: FSMContext):
    data = await state.get_data()
    language_code = data.get("language_code")
    language_text = await get_text(language_code, "CHANGE_LANGUAGE")
    await message.answer(
        language_text,
        reply_markup=await kb.language_keyboard(),
    )


@start_router.callback_query(F.data.startswith("lang_"))
async def set_language(callback_query: CallbackQuery, state: FSMContext):
    # Получаем выбранный язык
    language_code = callback_query.data.split("_")[1]
    await state.update_data(language_code=language_code)

    user_tg_id = callback_query.from_user.id
    # Обновляем язык в БД
    # await update_user_language(user_tg_id, language_code)

    await callback_query.message.delete()
    welcome_text = await get_text(language_code, "WELCOME_TEXT")
    await callback_query.message.answer(
        welcome_text, reply_markup=await kb.start_menu(language_code)
    )

    # Подтверждаем обработку callback
    language_update_text = await get_text(language_code, "LANGUAGE_UPDATE_TEXT")
    await callback_query.answer(text=language_update_text, show_alert=False)


@start_router.message(F.text.in_({"⁉️ Поддержка", "⁉️ Support"}))
async def start_support(message: Message, state: FSMContext):
    data = await state.get_data()
    language_code = data.get("language_code")
    support_text = await get_text(language_code, "SUPPORT")
    await message.answer(
        support_text, reply_markup=await kb.back_to_menu(language_code)
    )


@start_router.message(F.text.in_({"👥 Пригласить друзей", "👥 Invite friends"}))
async def back_to_menu(message: Message, state: FSMContext):
    data = await state.get_data()
    language_code = data.get("language_code")
    invite_text = await get_text(language_code, "INVITE")
    await message.answer(invite_text, reply_markup=await kb.back_to_menu(language_code))


@start_router.message(F.text.in_({"↩️ Назад в главное меню", "↩️ Back to main menu"}))
async def back_to_menu(message: Message, state: FSMContext):
    data = await state.get_data()
    language_code = data.get("language_code")
    welcome_text = await get_text(language_code, "WELCOME_TEXT")
    await message.answer(welcome_text, reply_markup=await kb.start_menu(language_code))
    await state.clear()
