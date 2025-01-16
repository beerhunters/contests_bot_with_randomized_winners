import json

from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tools.tools import send_localized_message
import keyboards.keyboards as kb

contest_router = Router()


class ContestState(StatesGroup):
    contest_channel = State()
    contest_text = State()
    contest_file = State()
    contest_winners_count = State()
    contest_post_time = State()
    contest_end_time = State()
    contest_location = State()
    contest_required_channels = State()
    contest_prizes = State()


@contest_router.message(F.text.in_({"🎁 Создать конкурс", "🎁 Create giveaway"}))
async def start_create(message: Message, state: FSMContext, l10n: FluentLocalization):
    await send_localized_message(message, l10n, "contest_channel")
    await state.set_state(ContestState.contest_channel)


@contest_router.message(ContestState.contest_channel)
async def add_channel(message: Message, state: FSMContext, l10n: FluentLocalization):

    contest_channel = message.text
    await state.update_data(contest_channel=contest_channel)

    await send_localized_message(message, l10n, "contest_text")
    await state.set_state(ContestState.contest_text)


@contest_router.message(ContestState.contest_text)
async def add_description(
    message: Message, state: FSMContext, l10n: FluentLocalization
):
    contest_text = message.text
    await state.update_data(contest_text=contest_text)

    await send_localized_message(message, l10n, "contest_file")
    await state.set_state(ContestState.contest_file)


@contest_router.message(ContestState.contest_file)
async def add_file(message: Message, state: FSMContext, l10n: FluentLocalization):
    if message.content_type == ContentType.PHOTO:
        file_id = message.photo[-1].file_id
        file_type = message.content_type
        await state.update_data(file_id=file_id, file_type=file_type)
    else:
        pass
    await send_localized_message(message, l10n, "contest_winners_count")
    await state.set_state(ContestState.contest_winners_count)


@contest_router.message(ContestState.contest_winners_count)
async def add_winners_count(
    message: Message, state: FSMContext, l10n: FluentLocalization
):
    try:
        winners_count = int(message.text)
        await state.update_data(winners_count=winners_count)

        await send_localized_message(message, l10n, "contest_post_time")
        await state.set_state(ContestState.contest_post_time)
    except ValueError:
        await send_localized_message(message, l10n, "invalid_contest_winners_count")


@contest_router.message(ContestState.contest_post_time)
async def add_post_time(message: Message, state: FSMContext, l10n: FluentLocalization):

    post_time = message.text
    await state.update_data(post_time=post_time)

    await send_localized_message(message, l10n, "contest_end_time")
    await state.set_state(ContestState.contest_end_time)


@contest_router.message(ContestState.contest_end_time)
async def add_end_time(message: Message, state: FSMContext, l10n: FluentLocalization):

    end_time = message.text
    await state.update_data(end_time=end_time)

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
    await send_localized_message(message, l10n, "contest_required_channels")
    await state.set_state(ContestState.contest_required_channels)


@contest_router.message(ContestState.contest_required_channels)
async def add_required_channels(
    message: Message, state: FSMContext, l10n: FluentLocalization
):

    required_channels = message.text
    await state.update_data(required_channels=required_channels)

    await send_localized_message(message, l10n, "contest_prizes")
    await state.set_state(ContestState.contest_prizes)


@contest_router.message(ContestState.contest_prizes)
async def add_prizes(message: Message, state: FSMContext, l10n: FluentLocalization):
    prizes = message.text
    await state.update_data(prizes=prizes)
    data = await state.get_data()
    # Выводим в формате JSON для удобства
    print(json.dumps(data, indent=4, ensure_ascii=False))


@contest_router.message(F.text.in_({"🎉 Мои розыгрыши", "🎉 My giveaways"}))
async def handle_my_contests(message: Message, state: FSMContext):
    """
    Обрабатывает команду "/my_contests".
    """
    await message.answer("В разработке", show_alert=True)
