import json

from aiogram import Router, F
from aiogram.enums import ContentType, ChatMemberStatus
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from fluent.runtime import FluentLocalization

from datetime import datetime

from tools.tools import send_localized_message, get_current_datetime
import keyboards.keyboards as kb
import keyboards.calendar_keyboard.custom_calendar as cl

contest_router = Router()


class ContestState(StatesGroup):
    contest_channel = State()
    contest_text = State()
    contest_file = State()
    contest_winners_count = State()
    contest_post_date = State()
    contest_post_time = State()
    contest_end_date = State()
    contest_end_time = State()
    contest_location = State()
    contest_required_channels = State()
    contest_prizes = State()


# Обработка кнопки старт
@contest_router.message(F.text.in_({"🎁 Создать конкурс", "🎁 Create giveaway"}))
async def start_create(message: Message, state: FSMContext, l10n: FluentLocalization):
    # await send_localized_message(message, l10n, "contest_channel")
    await send_localized_message(
        message, l10n, "contest_id", reply_markup=await kb.get_chat_id(l10n)
    )
    await state.set_state(ContestState.contest_channel)


# @contest_router.message(F.chat_shared, ContestState.contest_channel)
# async def add_channel(message: Message, state: FSMContext, l10n: FluentLocalization):
#     contest_channel = message.text.strip()
#
#     # Определяем chat_id
#     if contest_channel.startswith("@"):
#         chat_id = contest_channel  # Публичный юзернейм
#     elif contest_channel.lstrip("-").isdigit():
#         chat_id = int(contest_channel)  # Приватный ID канала
#     else:
#         await send_localized_message(message, l10n, "error_invalid_channel")
#         return
#
#     try:
#         # Получаем информацию о боте в указанном чате
#         chat_member = await message.bot.get_chat_member(
#             chat_id=chat_id, user_id=message.bot.id
#         )
#
#         # Проверяем, является ли бот администратором
#         if chat_member.status not in [
#             ChatMemberStatus.ADMINISTRATOR,
#             ChatMemberStatus.CREATOR,
#         ]:
#             await send_localized_message(message, l10n, "error_bot_not_admin")
#             return
#     except Exception as e:
#         # Обработка ошибок
#         if "chat not found" in str(e).lower():
#             await send_localized_message(message, l10n, "error_invalid_channel")
#         elif "access denied" in str(e).lower():
#             await send_localized_message(message, l10n, "error_bot_not_in_chat")
#         else:
#             await send_localized_message(message, l10n, "error_unexpected")
#         return
#
#     # Сохраняем данные и переходим к следующему состоянию
#     await state.update_data(contest_channel=contest_channel)
#     await send_localized_message(message, l10n, "contest_text")
#     await state.set_state(ContestState.contest_text)


# Записываем информацию о канале, спрашиваем про описание
@contest_router.message(F.chat_shared, ContestState.contest_channel)
async def add_channel(message: Message, state: FSMContext, l10n: FluentLocalization):
    chat_id = int(message.chat_shared.chat_id)

    try:
        # Получаем информацию о боте в указанном чате
        chat_member = await message.bot.get_chat_member(
            chat_id=chat_id, user_id=message.bot.id
        )

        # Проверяем, является ли бот администратором
        if chat_member.status not in [
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.CREATOR,
        ]:
            await send_localized_message(
                message,
                l10n,
                "error_bot_not_admin",
                reply_markup=await kb.get_chat_id(l10n),
            )
            return
    except Exception as e:
        # Обработка ошибок
        if "chat not found" in str(e).lower():
            await send_localized_message(
                message,
                l10n,
                "error_invalid_channel",
                reply_markup=await kb.get_chat_id(l10n),
            )
        elif "access denied" in str(e).lower():
            await send_localized_message(
                message,
                l10n,
                "error_bot_not_in_chat",
                reply_markup=await kb.get_chat_id(l10n),
            )
        else:
            await send_localized_message(
                message,
                l10n,
                "error_unexpected",
                reply_markup=await kb.get_chat_id(l10n),
            )
        return

    # Сохраняем данные и переходим к следующему состоянию
    await state.update_data(contest_channel=chat_id)
    await send_localized_message(message, l10n, "contest_chat_saved")
    await send_localized_message(message, l10n, "contest_text")
    await state.set_state(ContestState.contest_text)


# Записываем описание, спрашиваем про файл
@contest_router.message(ContestState.contest_text)
async def add_description(
    message: Message, state: FSMContext, l10n: FluentLocalization
):
    contest_text = message.text
    await state.update_data(contest_text=contest_text)
    await send_localized_message(message, l10n, "contest_description_saved")
    await send_localized_message(message, l10n, "contest_file")
    await state.set_state(ContestState.contest_file)


# Записываем файл, спрашиваем про количество участников
@contest_router.message(ContestState.contest_file)
async def add_file(message: Message, state: FSMContext, l10n: FluentLocalization):
    if message.content_type == ContentType.PHOTO:
        file_id = message.photo[-1].file_id
        file_type = "photo"
        await state.update_data(file_id=file_id, file_type=file_type)
    elif message.content_type == ContentType.VIDEO:
        file_id = message.video.file_id
        file_type = "video"
        await state.update_data(file_id=file_id, file_type=file_type)
    elif message.content_type == ContentType.STICKER:
        file_id = message.sticker.file_id
        file_type = "sticker"
        await state.update_data(file_id=file_id, file_type=file_type)
    elif message.content_type == ContentType.ANIMATION:
        file_id = message.animation.file_id
        file_type = "gif"
        await state.update_data(file_id=file_id, file_type=file_type)
    else:
        file_id = "unknown"
        file_type = "unknown"
        await state.update_data(file_id=file_id, file_type=file_type)
    if file_id and file_type != "unknown":
        await send_localized_message(message, l10n, "contest_attachment_saved")
    await send_localized_message(message, l10n, "contest_winners_count")
    await state.set_state(ContestState.contest_winners_count)


# Записываем кол-во участников, спрашиваем про время публикации
@contest_router.message(ContestState.contest_winners_count)
async def add_winners_count(
    message: Message, state: FSMContext, l10n: FluentLocalization
):
    try:
        winners_count = int(message.text)
        await state.update_data(winners_count=winners_count)
        await send_localized_message(message, l10n, "contest_winners_count_saved")
        # Спрашиваем, опубликовать сейчас или запланировать
        await send_localized_message(
            message,
            l10n,
            "contest_date_clarification",
            reply_markup=await kb.get_publish_keyboard(l10n),
        )
        await state.set_state(ContestState.contest_post_date)
    except ValueError:
        await send_localized_message(message, l10n, "invalid_contest_winners_count")


# Записываем время, если опубликовать прямо сейчас6 далее уточняем время завершения
@contest_router.callback_query(F.data == "publish_now", ContestState.contest_post_date)
async def add_post_date(
    callback: CallbackQuery, state: FSMContext, l10n: FluentLocalization
):
    await state.update_data(post_date="now")
    # post_time = post_date + post_time
    # по кол-ву участников или по времени
    calendar = cl.CustomCalendar()
    await send_localized_message(
        callback,
        l10n,
        "get_end_date",
        reply_markup=await calendar.generate_calendar(
            datetime.now().year,
            datetime.now().month,
            l10n=l10n,
        ),
    )
    await state.set_state(ContestState.contest_end_date)


# Выбираем дату завершения, так как пост будет запланированный
@contest_router.callback_query(
    F.data == "schedule_post", ContestState.contest_post_date
)
async def add_post_date(
    callback: CallbackQuery, state: FSMContext, l10n: FluentLocalization
):
    calendar = cl.CustomCalendar()
    await callback.message.edit_text(
        l10n.format_value("get_post_date"),
        reply_markup=await calendar.generate_calendar(
            datetime.now().year,
            datetime.now().month,
            l10n=l10n,
        ),
    )


@contest_router.callback_query(
    F.data.startswith("calendar:"), ContestState.contest_post_date
)
async def add_post_date(
    callback: CallbackQuery, state: FSMContext, l10n: FluentLocalization
):
    calendar = cl.CustomCalendar()
    selected_date = await calendar.handle_callback(callback, l10n=l10n)

    if selected_date:
        await state.update_data(post_date=selected_date.strftime("%d.%m.%Y"))
        # await callback.message.edit_text("Bыберите время:\n")
        await callback.answer()
        await send_localized_message(callback, l10n, "get_post_time")
        await state.set_state(ContestState.contest_post_time)


@contest_router.message(ContestState.contest_post_time)
async def add_post_time(message: Message, state: FSMContext, l10n: FluentLocalization):
    post_time = message.text
    # нужна проверка времени
    await state.update_data(post_time=post_time)
    # post_time = post_date + post_time
    # по кол-ву участников или по времени
    # await send_localized_message(message, l10n, "get_end_date")
    calendar = cl.CustomCalendar()
    await send_localized_message(
        message,
        l10n,
        "get_end_date",
        reply_markup=await calendar.generate_calendar(
            datetime.now().year,
            datetime.now().month,
            l10n=l10n,
        ),
    )
    await state.set_state(ContestState.contest_end_date)


@contest_router.callback_query(
    F.data.startswith("calendar:"), ContestState.contest_end_date
)
async def add_end_date(
    callback: CallbackQuery, state: FSMContext, l10n: FluentLocalization
):
    calendar = cl.CustomCalendar()
    selected_date = await calendar.handle_callback(callback, l10n=l10n)
    # if selected_date:
    #     await state.update_data(end_date=selected_date.strftime("%d.%m.%Y"))
    #     # await callback.message.edit_text("Bыберите время:\n")
    #     await callback.answer()
    #     await send_localized_message(callback, l10n, "get_end_time")
    #     await state.set_state(ContestState.contest_end_time)
    if selected_date:
        data = await state.get_data()
        post_date = data["post_date"]
        # Преобразуем post_date в объект datetime
        post_date_dt = datetime.strptime(post_date, "%d.%m.%Y")

        # Проверяем, что selected_date больше post_date
        if selected_date >= post_date_dt:
            # Обновляем состояние, если проверка успешна
            await state.update_data(end_date=selected_date.strftime("%d.%m.%Y"))
            await callback.answer()
            await send_localized_message(callback, l10n, "get_end_time")
            await state.set_state(ContestState.contest_end_time)
        else:
            # Если selected_date меньше или равна post_date, отправляем сообщение об ошибке
            await callback.answer(
                l10n.format_value("invalid_end_date"), show_alert=True
            )


# # Выбираем дату завершения, так как пост будет запланированный
# @contest_router.callback_query(
#     F.data == "schedule_post", ContestState.contest_post_time
# )
# async def add_post_time(message: Message, state: FSMContext, l10n: FluentLocalization):
#     post_time = message.text
#     await state.update_data(post_time=post_time)
#     # по кол-ву участников или по времени
#     await send_localized_message(message, l10n, "contest_end_time")
#     await state.set_state(ContestState.contest_end_time)


@contest_router.message(ContestState.contest_end_time)
async def add_end_time(message: Message, state: FSMContext, l10n: FluentLocalization):
    end_time = message.text
    # нужна двойная проверка времени
    await state.update_data(end_time=end_time)
    # post_time = post_date + post_time
    # вопрос нужна ли проверка ГЕО
    await send_localized_message(
        message,
        l10n,
        "contest_location",
        reply_markup=await kb.request_location_keyboard(l10n),
    )
    await state.set_state(ContestState.contest_location)


@contest_router.message(
    F.сontent_types.in_({ContentType.TEXT, ContentType.LOCATION})
    and ContestState.contest_location
)
async def add_location(message: Message, state: FSMContext, l10n: FluentLocalization):
    if message.content_type == ContentType.LOCATION:
        location = message.location
        latitude, longitude = location.latitude, location.longitude

        # Сохраняем локацию во временное состояние FSM
        await state.update_data(latitude=latitude, longitude=longitude)

        await message.answer(
            f"Геолокация успешно сохранена:\n"
            f"Широта: {latitude}\nДолгота: {longitude}",
        )
    else:
        pass
    await send_localized_message(message, l10n, "contest_prizes")
    await state.set_state(ContestState.contest_prizes)


@contest_router.message(ContestState.contest_prizes)
async def add_prizes(message: Message, state: FSMContext, l10n: FluentLocalization):
    prizes = message.text
    await state.update_data(prizes=prizes)
    await send_localized_message(message, l10n, "contest_required_channels")
    # клавиатура с кнопкой отказа от подписных каналов
    await state.set_state(ContestState.contest_required_channels)


@contest_router.message(ContestState.contest_required_channels)
async def add_required_channels(
    message: Message, state: FSMContext, l10n: FluentLocalization
):
    required_channels = message.text
    await state.update_data(required_channels=required_channels)
    data = await state.get_data()
    if data["post_time"] == "now":
        data["post_time"] = await get_current_datetime()
    # Если время "сейчас" проверять перед публикацией
    # Выводим в формате JSON для удобства
    print(json.dumps(data, indent=4, ensure_ascii=False))

    # итоговое сообщение перед публикацией/сохранением
    # действительно отменить?
    # await send_localized_message(message, l10n, "contest_prizes")
    # await state.set_state(ContestState.contest_prizes)


@contest_router.message(F.text.in_({"🎉 Мои розыгрыши", "🎉 My giveaways"}))
async def handle_my_contests(message: Message, state: FSMContext):
    """
    Обрабатывает команду "/my_contests".
    """
    await message.answer("В разработке", show_alert=True)
