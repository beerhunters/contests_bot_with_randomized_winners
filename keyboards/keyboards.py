from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
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


async def back_to_menu(l10n: FluentLocalization):
    button_text = l10n.format_value("back-to-menu")
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=button_text)]],
        resize_keyboard=True,
    )


# async def language_keyboard():
#     return InlineKeyboardMarkup(
#         inline_keyboard=[
#             [
#                 InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
#                 InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en"),
#             ]
#         ]
#     )
