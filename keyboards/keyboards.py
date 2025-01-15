from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from configs.texts import menu_texts


async def start_menu(language_code: str):
    buttons = menu_texts.get(language_code, menu_texts["ru"])["MENU_BUTTONS"]

    # Формируем ряды кнопок: 2 кнопки, 1 кнопка, 2 кнопки
    keyboard_layout = [
        [
            KeyboardButton(text=buttons[0]),
            KeyboardButton(text=buttons[1]),
        ],  # Первый ряд: 2 кнопки
        [KeyboardButton(text=buttons[2])],  # Второй ряд: 1 кнопка
        [
            KeyboardButton(text=buttons[3]),
            KeyboardButton(text=buttons[4]),
        ],  # Третий ряд: 2 кнопки
    ]

    return ReplyKeyboardMarkup(
        keyboard=keyboard_layout,
        resize_keyboard=True,
    )


async def back_to_menu(language_code: str):
    button_text = menu_texts.get(language_code, menu_texts["ru"])["BACK_TO_MENU"]
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=button_text)]],
        resize_keyboard=True,
    )


async def language_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
                InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en"),
            ]
        ]
    )
