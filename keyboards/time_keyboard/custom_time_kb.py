# from aiogram import Router, types
# from aiogram.filters.callback_data import CallbackData
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# from aiogram.utils.keyboard import InlineKeyboardBuilder
#
# time_selector = Router()
#
#
# # CallbackData для клавиатуры
# class TimeCallback(CallbackData, prefix="time"):
#     action: str  # up, down, back, select
#     target: str  # hour1, hour2, min1, min2
#
#
# # Хранилище выбранного времени
# user_time = {"hour1": 0, "hour2": 0, "min1": 0, "min2": 0}
#
#
# # Создание клавиатуры
# async def create_time_keyboard():
#     builder = InlineKeyboardBuilder()
#
#     # Верхний ряд стрелок
#     builder.row(
#         InlineKeyboardButton(
#             text="▲", callback_data=TimeCallback(action="up", target="hour1").pack()
#         ),
#         InlineKeyboardButton(
#             text="▲", callback_data=TimeCallback(action="up", target="hour2").pack()
#         ),
#         InlineKeyboardButton(text=" ", callback_data="noop"),  # Пустая кнопка
#         InlineKeyboardButton(
#             text="▲", callback_data=TimeCallback(action="up", target="min1").pack()
#         ),
#         InlineKeyboardButton(
#             text="▲", callback_data=TimeCallback(action="up", target="min2").pack()
#         ),
#     )
#
#     # Числа с двоеточием
#     builder.row(
#         InlineKeyboardButton(text=f"{user_time['hour1']}", callback_data="noop"),
#         InlineKeyboardButton(text=f"{user_time['hour2']}", callback_data="noop"),
#         InlineKeyboardButton(text=":", callback_data="noop"),
#         InlineKeyboardButton(text=f"{user_time['min1']}", callback_data="noop"),
#         InlineKeyboardButton(text=f"{user_time['min2']}", callback_data="noop"),
#     )
#
#     # Нижний ряд стрелок
#     builder.row(
#         InlineKeyboardButton(
#             text="▼", callback_data=TimeCallback(action="down", target="hour1").pack()
#         ),
#         InlineKeyboardButton(
#             text="▼", callback_data=TimeCallback(action="down", target="hour2").pack()
#         ),
#         InlineKeyboardButton(text=" ", callback_data="noop"),  # Пустая кнопка
#         InlineKeyboardButton(
#             text="▼", callback_data=TimeCallback(action="down", target="min1").pack()
#         ),
#         InlineKeyboardButton(
#             text="▼", callback_data=TimeCallback(action="down", target="min2").pack()
#         ),
#     )
#
#     # Кнопки Назад и Выбрать
#     builder.row(
#         InlineKeyboardButton(
#             text="Назад",
#             callback_data=TimeCallback(action="back", target="none").pack(),
#         ),
#         InlineKeyboardButton(
#             text="Выбрать",
#             callback_data=TimeCallback(action="select", target="none").pack(),
#         ),
#     )
#
#     return builder.as_markup()
#
#
# # Обработчик клавиатуры
# @time_selector.callback_query(TimeCallback.filter())
# async def handle_time_callback(
#     callback: types.CallbackQuery, callback_data: TimeCallback
# ):
#     global user_time
#
#     # Получение текущего значения
#     if callback_data.target != "none":
#         current_value = user_time[callback_data.target]
#
#     # Логика изменения значений
#     if callback_data.action == "up":
#         if callback_data.target.startswith("hour"):
#             max_value = (
#                 2 if callback_data.target == "hour1" and user_time["hour2"] > 3 else 9
#             )
#         else:
#             max_value = 9
#         user_time[callback_data.target] = (current_value + 1) % (max_value + 1)
#
#     elif callback_data.action == "down":
#         if callback_data.target.startswith("hour"):
#             max_value = (
#                 2 if callback_data.target == "hour1" and user_time["hour2"] > 3 else 9
#             )
#         else:
#             max_value = 9
#         user_time[callback_data.target] = (current_value - 1) % (max_value + 1)
#
#     # Ограничения времени
#     hours = int(f"{user_time['hour1']}{user_time['hour2']}")
#     minutes = int(f"{user_time['min1']}{user_time['min2']}")
#
#     if hours > 23:
#         user_time["hour1"], user_time["hour2"] = 2, 3
#     if minutes > 59:
#         user_time["min1"], user_time["min2"] = 5, 9
#
#     # Действие на кнопках
#     if callback_data.action == "select":
#         # selected_time = f"{hours:02}:{minutes:02}"
#         await callback.message.answer(f"Вы выбрали время: {hours:02}:{minutes:02}")
#         # return selected_time
#     elif callback_data.action == "back":
#         await callback.message.answer("Возвращаемся назад.")
#     else:
#         # Обновление клавиатуры
#         await callback.message.edit_reply_markup(reply_markup=await create_time_keyboard())
#
#     await callback.answer()
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder


class TimeCallback(CallbackData, prefix="time"):
    """Класс для обработки callback_data."""

    action: str  # up, down, back, select
    target: str  # hour1, hour2, min1, min2


class TimePicker:
    """Класс для создания инлайн-клавиатуры выбора времени и обработки колбэков."""

    def __init__(self):
        self.user_time = {"hour1": 0, "hour2": 0, "min1": 0, "min2": 0}

    async def create_time_keyboard(self) -> InlineKeyboardMarkup:
        """Создает инлайн-клавиатуру для выбора времени."""
        builder = InlineKeyboardBuilder()

        # Верхний ряд стрелок
        builder.row(
            InlineKeyboardButton(
                text="▲", callback_data=TimeCallback(action="up", target="hour1").pack()
            ),
            InlineKeyboardButton(
                text="▲", callback_data=TimeCallback(action="up", target="hour2").pack()
            ),
            InlineKeyboardButton(text=" ", callback_data="noop"),  # Пустая кнопка
            InlineKeyboardButton(
                text="▲", callback_data=TimeCallback(action="up", target="min1").pack()
            ),
            InlineKeyboardButton(
                text="▲", callback_data=TimeCallback(action="up", target="min2").pack()
            ),
        )

        # Числа с двоеточием
        builder.row(
            InlineKeyboardButton(
                text=f"{self.user_time['hour1']}", callback_data="noop"
            ),
            InlineKeyboardButton(
                text=f"{self.user_time['hour2']}", callback_data="noop"
            ),
            InlineKeyboardButton(text=":", callback_data="noop"),
            InlineKeyboardButton(
                text=f"{self.user_time['min1']}", callback_data="noop"
            ),
            InlineKeyboardButton(
                text=f"{self.user_time['min2']}", callback_data="noop"
            ),
        )

        # Нижний ряд стрелок
        builder.row(
            InlineKeyboardButton(
                text="▼",
                callback_data=TimeCallback(action="down", target="hour1").pack(),
            ),
            InlineKeyboardButton(
                text="▼",
                callback_data=TimeCallback(action="down", target="hour2").pack(),
            ),
            InlineKeyboardButton(text=" ", callback_data="noop"),  # Пустая кнопка
            InlineKeyboardButton(
                text="▼",
                callback_data=TimeCallback(action="down", target="min1").pack(),
            ),
            InlineKeyboardButton(
                text="▼",
                callback_data=TimeCallback(action="down", target="min2").pack(),
            ),
        )

        # Кнопки Назад и Выбрать
        builder.row(
            InlineKeyboardButton(
                text=" ",
                callback_data=TimeCallback(action=" ", target="none").pack(),
            ),
            InlineKeyboardButton(
                text="Выбрать",
                callback_data=TimeCallback(action="select", target="none").pack(),
            ),
        )

        return builder.as_markup()

    async def handle_callback(
        self, callback: CallbackQuery, callback_data: TimeCallback
    ):
        """Обрабатывает нажатия на кнопки."""
        # Получение текущего значения
        if callback_data.target != "none":
            current_value = self.user_time[callback_data.target]

        # Логика изменения значений
        if callback_data.action == "up":
            max_value = (
                2
                if callback_data.target == "hour1" and self.user_time["hour2"] > 3
                else 9
            )
            self.user_time[callback_data.target] = (current_value + 1) % (max_value + 1)

        elif callback_data.action == "down":
            max_value = (
                2
                if callback_data.target == "hour1" and self.user_time["hour2"] > 3
                else 9
            )
            self.user_time[callback_data.target] = (current_value - 1) % (max_value + 1)

        # Ограничения времени
        hours = int(f"{self.user_time['hour1']}{self.user_time['hour2']}")
        minutes = int(f"{self.user_time['min1']}{self.user_time['min2']}")

        if hours > 23:
            self.user_time["hour1"], self.user_time["hour2"] = 2, 3
        if minutes > 59:
            self.user_time["min1"], self.user_time["min2"] = 5, 9

        # Действие на кнопках
        if callback_data.action == "select":
            selected_time = f"{hours:02}:{minutes:02}"
            # await callback.message.answer(f"Вы выбрали время: {selected_time}")
            print(selected_time)
            return selected_time
        elif callback_data.action == "back":
            print("back")
            # await callback.message.answer("Возвращаемся назад.")
        else:
            # Обновление клавиатуры
            await callback.message.edit_reply_markup(
                reply_markup=await self.create_time_keyboard()
            )

        await callback.answer()
