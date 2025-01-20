from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    # InlineKeyboardMarkup,
    # InlineKeyboardButton,
    KeyboardButtonRequestChat,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from fluent.runtime import FluentLocalization


async def start_menu(l10n: FluentLocalization):
    # Получаем локализованные тексты для кнопок
    buttons = [
        l10n.format_value("menu-create-giveaway"),
        l10n.format_value("menu-my-giveaways"),
        l10n.format_value("menu-support"),
        l10n.format_value("menu-invite-friends"),
    ]

    # Формируем ряды кнопок: 2 кнопки, 1 кнопка, 2 кнопки
    keyboard_layout = [
        [
            KeyboardButton(text=buttons[0]),
            KeyboardButton(text=buttons[1]),
        ],  # Первый ряд: 2 кнопки
        # [KeyboardButton(text=buttons[2])],  # Второй ряд: 1 кнопка
        [
            KeyboardButton(text=buttons[2]),
            KeyboardButton(text=buttons[3]),
        ],  # Третий ряд: 2 кнопки
    ]

    return ReplyKeyboardMarkup(
        keyboard=keyboard_layout,
        resize_keyboard=True,
    )


async def get_chat_id(l10n, one_time_keyboard=True):
    buttons = [
        [
            KeyboardButton(
                text=l10n.format_value("chat-id"),
                request_chat=KeyboardButtonRequestChat(
                    request_id=0,
                    chat_is_channel=False,  # Включает только обычные группы (не каналы)
                    bot_is_member=True,
                ),
            ),
            KeyboardButton(
                text=l10n.format_value("channel-id"),
                request_chat=KeyboardButtonRequestChat(
                    request_id=1, chat_is_channel=True  # Включает только каналы
                ),
            ),
        ],
    ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=one_time_keyboard,
    )

    return keyboard


async def back_to_menu(l10n: FluentLocalization):
    button_text = l10n.format_value("back-to-menu")
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=button_text)]],
        resize_keyboard=True,
    )


async def get_publish_keyboard(l10n) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=l10n.format_value("publish_now"), callback_data="publish_now")
    keyboard.button(
        text=l10n.format_value("schedule_post"), callback_data="schedule_post"
    )
    return keyboard.as_markup(row_width=2)


async def geo_check_required(l10n) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(  # Добавляем первую кнопку в строку
        InlineKeyboardButton(text=l10n.format_value("geo_yes"), callback_data="geo_yes")
    )
    keyboard.row(  # Добавляем вторую кнопку в новую строку
        InlineKeyboardButton(text=l10n.format_value("geo_no"), callback_data="geo_no")
    )
    return keyboard.as_markup()


async def request_location_keyboard(l10n: FluentLocalization):
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=l10n.format_value("location"), request_location=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


async def publish_now(l10n) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=l10n.format_value("yes"), callback_data="yes")
    keyboard.button(text=l10n.format_value("no"), callback_data="no")
    return keyboard.as_markup(row_width=2)


async def participation(l10n) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text=l10n.format_value("participation"), callback_data="participation"
    )
    return keyboard.as_markup()


# async def participation(l10n, participants_count: int) -> InlineKeyboardMarkup:
#     keyboard = InlineKeyboardBuilder()
#
#     # Формируем текст с количеством участников
#     participation_text = f"{l10n.format_value('participation')} ({participants_count})"
#
#     keyboard.button(
#         text=participation_text, callback_data="participation"
#     )
#     return keyboard.as_markup()
