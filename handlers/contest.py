import html
import json

from aiogram import Router, F
from aiogram.enums import ContentType, ChatMemberStatus, ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from fluent.runtime import FluentLocalization

from datetime import datetime, timedelta

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
    contest_confirmation = State()
    contest_cancel_confirmation = State()


# Обработка кнопки старт
@contest_router.message(F.text.in_({"🎁 Создать конкурс", "🎁 Create giveaway"}))
async def start_create(message: Message, state: FSMContext, l10n: FluentLocalization):
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

    data = await state.get_data()
    required_channels = data.get("required_channels", [])
    required_channels.append(str(chat_id))
    await state.update_data(required_channels=required_channels)

    await send_localized_message(message, l10n, "contest_data_saved")
    await send_localized_message(message, l10n, "contest_text")
    await state.set_state(ContestState.contest_text)


# Записываем описание, спрашиваем про файл
@contest_router.message(ContestState.contest_text)
async def add_description(
    message: Message, state: FSMContext, l10n: FluentLocalization
):
    contest_text = message.text
    await state.update_data(contest_text=contest_text)
    await send_localized_message(message, l10n, "contest_data_saved")
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
        await send_localized_message(message, l10n, "contest_data_saved")
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
        await send_localized_message(message, l10n, "contest_data_saved")
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
    # Получаем текущую дату и время в формате "%d.%m.%Y %H:%M"
    post_date = datetime.now().strftime("%d.%m.%Y")
    post_time = datetime.now().strftime("%H:%M")
    await state.update_data(post_date=post_date, post_time=post_time, post="now")
    await send_localized_message(callback, l10n, "contest_data_saved", show_alert=True)
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
    await state.update_data(post="schedule")
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
        today = datetime.today().date()

        # Проверяем, что выбранная дата больше текущей
        if selected_date.date() >= today:
            await state.update_data(post_date=selected_date.strftime("%d.%m.%Y"))
            await send_localized_message(
                callback, l10n, "contest_data_saved", show_alert=True
            )
            await callback.answer()
            await send_localized_message(callback, l10n, "get_post_time")
            await state.set_state(ContestState.contest_post_time)
        else:
            # Если дата меньше сегодняшней, показываем сообщение об ошибке
            await callback.answer(
                l10n.format_value("error_date_in_past"), show_alert=True
            )


@contest_router.message(ContestState.contest_post_time)
async def add_post_time(message: Message, state: FSMContext, l10n: FluentLocalization):
    try:
        # Получаем текущее время
        now = datetime.now()

        # Парсим время, введенное пользователем
        post_time = datetime.strptime(message.text, "%H:%M").time()

        # Проверяем, что введенное время больше текущего
        if post_time > now.time():
            await state.update_data(post_time=message.text)
            await send_localized_message(message, l10n, "contest_data_saved")
            # Отправляем календарь для выбора даты окончания
            calendar = cl.CustomCalendar()
            await send_localized_message(
                message,
                l10n,
                "get_end_date",
                reply_markup=await calendar.generate_calendar(
                    now.year,
                    now.month,
                    l10n=l10n,
                ),
            )
            await state.set_state(ContestState.contest_end_date)
        else:
            # Время введено некорректно
            await send_localized_message(message, l10n, "error_time_in_past")
    except ValueError:
        # Если формат времени некорректный
        await send_localized_message(message, l10n, "error_invalid_time_format")


@contest_router.callback_query(
    F.data.startswith("calendar:"), ContestState.contest_end_date
)
async def add_end_date(
    callback: CallbackQuery, state: FSMContext, l10n: FluentLocalization
):
    calendar = cl.CustomCalendar()
    selected_date = await calendar.handle_callback(callback, l10n=l10n)

    if selected_date:
        data = await state.get_data()
        post_date = data["post_date"]
        # Преобразуем post_date в объект datetime
        post_date_dt = datetime.strptime(post_date, "%d.%m.%Y")

        # Проверяем, что selected_date больше post_date
        if selected_date >= post_date_dt:
            # Обновляем состояние, если проверка успешна
            await state.update_data(end_date=selected_date.strftime("%d.%m.%Y"))
            await send_localized_message(
                callback, l10n, "contest_data_saved", show_alert=True
            )
            await callback.answer()
            await send_localized_message(callback, l10n, "get_end_time")
            await state.set_state(ContestState.contest_end_time)
        else:
            # Если selected_date меньше или равна post_date, отправляем сообщение об ошибке
            await callback.answer(
                l10n.format_value("invalid_end_date"), show_alert=True
            )


@contest_router.message(ContestState.contest_end_time)
async def add_end_time(message: Message, state: FSMContext, l10n: FluentLocalization):
    try:
        # Парсим время, введённое пользователем
        # print(f"Raw input: {message.text}")
        end_time = datetime.strptime(message.text.strip(), "%H:%M").time()
        # print(f"Parsed end_time: {end_time}")

        # Получаем данные из состояния
        data = await state.get_data()

        # Преобразуем даты и время из формата `"%d.%m.%Y"` и `"%H:%M"`
        post_time = datetime.strptime(data["post_time"], "%H:%M").time()
        post_date = datetime.strptime(data["post_date"], "%d.%m.%Y").date()
        end_date = datetime.strptime(data["end_date"], "%d.%m.%Y").date()
        # print(f"Post time: {post_time}, Post date: {post_date}, End date: {end_date}")

        # Проверка на совпадение дат
        if post_date == end_date:
            post_datetime = datetime.combine(post_date, post_time)
            end_datetime = datetime.combine(end_date, end_time)

            # Проверяем разницу во времени
            if end_datetime - post_datetime < timedelta(minutes=10):
                await send_localized_message(message, l10n, "error_time_too_close")
                return

        elif post_date > end_date:
            await send_localized_message(message, l10n, "error_invalid_date_order")
            return

        # Сохраняем данные, если все проверки пройдены
        await state.update_data(end_time=message.text)
        await send_localized_message(message, l10n, "contest_data_saved")
        await send_localized_message(
            message,
            l10n,
            "contest_geo_check_required",
            reply_markup=await kb.geo_check_required(l10n),
        )
        await state.set_state(ContestState.contest_location)

    except ValueError as e:
        # Отладка ошибки
        # print(f"ValueError occurred: {e}")
        await send_localized_message(message, l10n, "error_invalid_time_format")


@contest_router.callback_query(F.data == "geo_yes", ContestState.contest_location)
async def add_location(
    callback: CallbackQuery, state: FSMContext, l10n: FluentLocalization
):
    await send_localized_message(
        callback,
        l10n,
        "contest_location",
        reply_markup=await kb.request_location_keyboard(l10n),
    )
    await state.set_state(ContestState.contest_location)


@contest_router.message(
    F.content_type.in_({ContentType.TEXT, ContentType.LOCATION})
    and ContestState.contest_location
)
async def add_location(message: Message, state: FSMContext, l10n: FluentLocalization):
    try:
        if message.content_type == ContentType.LOCATION:
            location = message.location
            if not location:
                # Если данные о местоположении отсутствуют
                await send_localized_message(message, l10n, "error_no_location")
                return

            # Проверяем корректность широты и долготы
            latitude, longitude = location.latitude, location.longitude
            if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
                await send_localized_message(message, l10n, "error_invalid_location")
                return

            # Сохраняем локацию во временное состояние FSM
            await state.update_data(latitude=latitude, longitude=longitude)

            print(
                f"Геолокация успешно сохранена:\n"
                f"Широта: {latitude}\nДолгота: {longitude}",
            )
        else:
            # Если получен текст вместо локации
            await send_localized_message(message, l10n, "error_location_required")
            return

        # Успешное сохранение данных
        await send_localized_message(message, l10n, "contest_data_saved")
        await send_localized_message(message, l10n, "contest_prizes")
        await state.set_state(ContestState.contest_prizes)

    except Exception as e:
        # Логирование ошибки и сообщение пользователю
        print(f"Ошибка обработки геолокации: {e}")
        await send_localized_message(message, l10n, "error_processing_location")


@contest_router.callback_query(F.data == "geo_no", ContestState.contest_location)
async def no_add_location(
    callback: CallbackQuery, state: FSMContext, l10n: FluentLocalization
):
    await send_localized_message(callback, l10n, "contest_data_saved")
    await send_localized_message(callback, l10n, "contest_prizes")
    await state.set_state(ContestState.contest_prizes)


@contest_router.message(ContestState.contest_prizes)
async def add_prizes(message: Message, state: FSMContext, l10n: FluentLocalization):
    try:
        # Получаем текст из сообщения
        prizes_text = message.text.strip()

        # Проверяем, что текст не пустой
        if not prizes_text:
            await send_localized_message(message, l10n, "error_empty_prizes")
            return

        # Разбиваем строку на список призов, удаляем лишние пробелы
        prizes = [prize.strip() for prize in prizes_text.split(",") if prize.strip()]

        # Проверяем, что список не пустой после обработки
        if not prizes:
            await send_localized_message(message, l10n, "error_empty_prizes")
            return

        # Сохраняем список призов в состояние FSM
        await state.update_data(prizes=prizes)

        # Уведомляем пользователя об успешном сохранении
        await send_localized_message(message, l10n, "contest_data_saved")

        # Переходим к следующему шагу
        await send_localized_message(
            message,
            l10n,
            "contest_required_channels",
            reply_markup=await kb.get_chat_id(l10n, one_time_keyboard=False),
        )
        await state.set_state(ContestState.contest_required_channels)

    except Exception as e:
        # Обрабатываем любые непредвиденные ошибки
        print(f"Ошибка обработки призов: {e}")
        await send_localized_message(message, l10n, "error_processing_prizes")


@contest_router.message(ContestState.contest_required_channels)
async def add_required_channels(
    message: Message, state: FSMContext, l10n: FluentLocalization
):
    try:
        # Проверяем, что сообщение содержит chat_id, полученный через клавиатуру
        if message.chat_shared:
            # Это означает, что пользователь выбрал канал или группу через клавиатуру
            required_channels_text = str(message.chat_shared.chat_id)
        elif message.text:
            # Если пользователь прислал текст (возможно, имя канала)
            required_channels_text = message.text.strip()
        else:
            # Если сообщение пустое, ничего не делаем
            return

        # Если пользователь отправил команду "/stop", завершаем процесс и переходим к следующему этапу
        if required_channels_text == "/stop":
            # Завершаем сбор каналов и переходим к следующему шагу
            await send_localized_message(
                message,
                l10n,
                "contest_channels_done",
                reply_markup=await kb.publish_now(l10n),
            )
            await state.set_state(ContestState.contest_confirmation)
            return

        # Получаем текущие данные состояния
        data = await state.get_data()
        required_channels = data.get("required_channels", [])

        # Проверяем, не добавлен ли уже такой канал/группа
        if required_channels_text in required_channels:
            # Если канал уже в списке, уведомляем пользователя
            await send_localized_message(
                message, l10n, "contest_channel_already_been_added"
            )
            return
        else:
            # Добавляем новый канал/группу в список
            required_channels.append(required_channels_text)

            # Сохраняем обновлённый список в состояние FSM
            await state.update_data(required_channels=required_channels)

            # Проверяем, если это не последний канал, снова показываем клавиатуру для добавления других каналов
            await send_localized_message(
                message,
                l10n,
                "contest_channel_added",
                reply_markup=await kb.get_chat_id(l10n, one_time_keyboard=False),
            )

    except Exception as e:
        print(f"Ошибка обработки каналов/групп: {e}")
        await send_localized_message(message, l10n, "error_processing_channels")


@contest_router.callback_query(F.data == "yes", ContestState.contest_confirmation)
async def contest_confirmation(
    callback: CallbackQuery, state: FSMContext, l10n: FluentLocalization
):
    await callback.answer("🎉 Confirmation!", show_alert=True)
    # Здесь надо сохранить все в БД и дальше работать с данными из БД
    data = await state.get_data()
    if data["post_time"] == "now":
        data["post_time"] = await get_current_datetime()
    else:
        # Конвертация времени публикации в datetime
        data["post_time"] = datetime.strptime(
            f"{data['post_date']} {data['post_time']}", "%d.%m.%Y %H:%M"
        )
    data["end_time"] = datetime.strptime(
        f"{data['end_date']} {data['end_time']}", "%d.%m.%Y %H:%M"
    )
    # Преобразуем datetime в строку для сериализации
    serialized_data = {
        key: (
            value.strftime("%d.%m.%Y %H:%M") if isinstance(value, datetime) else value
        )
        for key, value in data.items()
    }
    # Отправка данных в чат конкурса
    contest_channel_id = int(data["contest_channel"])  # Преобразуем ID в int
    contest_message = "<b>Данные конкурса:</b>\n"

    # Форматируем данные для HTML-разметки
    for key, value in serialized_data.items():
        contest_message += (
            f"<b>{key}:</b> {html.escape(str(value))}\n"  # Экранируем символы
        )
    if data["post"] == "now":
        await send_localized_message(callback, l10n, "publish_now_welcome")
        # Отправка данных в чат
        await callback.bot.send_message(
            chat_id=contest_channel_id,
            text=contest_message,
            reply_markup=await kb.participation(l10n),
            parse_mode=ParseMode.HTML,
        )
    else:
        post_date = data["post_time"].strftime("%d.%m.%Y")
        post_time = data["post_time"].strftime("%H:%M")

        # Формируем текст с локализацией
        text = l10n.format_value(
            "schedule_welcome", {"date": post_date, "time": post_time}
        )
        await callback.message.edit_text(text)

        # Нужна логика отложенных сообщений, пока заглушка
        await callback.bot.send_message(
            chat_id=contest_channel_id,
            text=text,
            parse_mode=ParseMode.HTML,
        )

    await send_localized_message(
        callback, l10n, "welcome_text", reply_markup=await kb.start_menu(l10n)
    )
    await state.clear()


@contest_router.callback_query(F.data == "no", ContestState.contest_confirmation)
async def contest_confirmation(
    callback: CallbackQuery, state: FSMContext, l10n: FluentLocalization
):
    await send_localized_message(
        callback,
        l10n,
        "contest_cancel_confirmation",
        reply_markup=await kb.publish_now(l10n),
    )
    await state.set_state(ContestState.contest_cancel_confirmation)


@contest_router.callback_query(
    F.data == "yes", ContestState.contest_cancel_confirmation
)
async def contest_confirmation(
    callback: CallbackQuery, state: FSMContext, l10n: FluentLocalization
):
    await callback.answer("☹️ Okay..", show_alert=True)
    await send_localized_message(
        callback, l10n, "welcome_text", reply_markup=await kb.start_menu(l10n)
    )
    await state.clear()


@contest_router.callback_query(F.data == "no", ContestState.contest_cancel_confirmation)
async def contest_confirmation(
    callback: CallbackQuery, state: FSMContext, l10n: FluentLocalization
):
    await send_localized_message(
        callback,
        l10n,
        "contest_repeat_confirmation",
        reply_markup=await kb.publish_now(l10n),
    )
    await state.set_state(ContestState.contest_confirmation)
