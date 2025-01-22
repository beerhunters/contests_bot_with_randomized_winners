# # # # from aiogram import Router, types
# # # # from aiogram.filters.callback_data import CallbackData
# # # # from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# # # # from aiogram.utils.keyboard import InlineKeyboardBuilder
# # # #
# # # # time_selector = Router()
# # # #
# # # #
# # # # # CallbackData для клавиатуры
# # # # class TimeCallback(CallbackData, prefix="time"):
# # # #     action: str  # up, down, back, select
# # # #     target: str  # hour1, hour2, min1, min2
# # # #
# # # #
# # # # # Хранилище выбранного времени
# # # # user_time = {"hour1": 0, "hour2": 0, "min1": 0, "min2": 0}
# # # #
# # # #
# # # # # Создание клавиатуры
# # # # async def create_time_keyboard():
# # # #     builder = InlineKeyboardBuilder()
# # # #
# # # #     # Верхний ряд стрелок
# # # #     builder.row(
# # # #         InlineKeyboardButton(
# # # #             text="▲", callback_data=TimeCallback(action="up", target="hour1").pack()
# # # #         ),
# # # #         InlineKeyboardButton(
# # # #             text="▲", callback_data=TimeCallback(action="up", target="hour2").pack()
# # # #         ),
# # # #         InlineKeyboardButton(text=" ", callback_data="noop"),  # Пустая кнопка
# # # #         InlineKeyboardButton(
# # # #             text="▲", callback_data=TimeCallback(action="up", target="min1").pack()
# # # #         ),
# # # #         InlineKeyboardButton(
# # # #             text="▲", callback_data=TimeCallback(action="up", target="min2").pack()
# # # #         ),
# # # #     )
# # # #
# # # #     # Числа с двоеточием
# # # #     builder.row(
# # # #         InlineKeyboardButton(text=f"{user_time['hour1']}", callback_data="noop"),
# # # #         InlineKeyboardButton(text=f"{user_time['hour2']}", callback_data="noop"),
# # # #         InlineKeyboardButton(text=":", callback_data="noop"),
# # # #         InlineKeyboardButton(text=f"{user_time['min1']}", callback_data="noop"),
# # # #         InlineKeyboardButton(text=f"{user_time['min2']}", callback_data="noop"),
# # # #     )
# # # #
# # # #     # Нижний ряд стрелок
# # # #     builder.row(
# # # #         InlineKeyboardButton(
# # # #             text="▼", callback_data=TimeCallback(action="down", target="hour1").pack()
# # # #         ),
# # # #         InlineKeyboardButton(
# # # #             text="▼", callback_data=TimeCallback(action="down", target="hour2").pack()
# # # #         ),
# # # #         InlineKeyboardButton(text=" ", callback_data="noop"),  # Пустая кнопка
# # # #         InlineKeyboardButton(
# # # #             text="▼", callback_data=TimeCallback(action="down", target="min1").pack()
# # # #         ),
# # # #         InlineKeyboardButton(
# # # #             text="▼", callback_data=TimeCallback(action="down", target="min2").pack()
# # # #         ),
# # # #     )
# # # #
# # # #     # Кнопки Назад и Выбрать
# # # #     builder.row(
# # # #         InlineKeyboardButton(
# # # #             text="Назад",
# # # #             callback_data=TimeCallback(action="back", target="none").pack(),
# # # #         ),
# # # #         InlineKeyboardButton(
# # # #             text="Выбрать",
# # # #             callback_data=TimeCallback(action="select", target="none").pack(),
# # # #         ),
# # # #     )
# # # #
# # # #     return builder.as_markup()
# # # #
# # # #
# # # # # Обработчик клавиатуры
# # # # @time_selector.callback_query(TimeCallback.filter())
# # # # async def handle_time_callback(
# # # #     callback: types.CallbackQuery, callback_data: TimeCallback
# # # # ):
# # # #     global user_time
# # # #
# # # #     # Получение текущего значения
# # # #     if callback_data.target != "none":
# # # #         current_value = user_time[callback_data.target]
# # # #
# # # #     # Логика изменения значений
# # # #     if callback_data.action == "up":
# # # #         if callback_data.target.startswith("hour"):
# # # #             max_value = (
# # # #                 2 if callback_data.target == "hour1" and user_time["hour2"] > 3 else 9
# # # #             )
# # # #         else:
# # # #             max_value = 9
# # # #         user_time[callback_data.target] = (current_value + 1) % (max_value + 1)
# # # #
# # # #     elif callback_data.action == "down":
# # # #         if callback_data.target.startswith("hour"):
# # # #             max_value = (
# # # #                 2 if callback_data.target == "hour1" and user_time["hour2"] > 3 else 9
# # # #             )
# # # #         else:
# # # #             max_value = 9
# # # #         user_time[callback_data.target] = (current_value - 1) % (max_value + 1)
# # # #
# # # #     # Ограничения времени
# # # #     hours = int(f"{user_time['hour1']}{user_time['hour2']}")
# # # #     minutes = int(f"{user_time['min1']}{user_time['min2']}")
# # # #
# # # #     if hours > 23:
# # # #         user_time["hour1"], user_time["hour2"] = 2, 3
# # # #     if minutes > 59:
# # # #         user_time["min1"], user_time["min2"] = 5, 9
# # # #
# # # #     # Действие на кнопках
# # # #     if callback_data.action == "select":
# # # #         # selected_time = f"{hours:02}:{minutes:02}"
# # # #         await callback.message.answer(f"Вы выбрали время: {hours:02}:{minutes:02}")
# # # #         # return selected_time
# # # #     elif callback_data.action == "back":
# # # #         await callback.message.answer("Возвращаемся назад.")
# # # #     else:
# # # #         # Обновление клавиатуры
# # # #         await callback.message.edit_reply_markup(reply_markup=await create_time_keyboard())
# # # #
# # # #     await callback.answer()
# # # from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
# # # from aiogram.filters.callback_data import CallbackData
# # # from aiogram.utils.keyboard import InlineKeyboardBuilder
# # #
# # #
# # # class TimeCallback(CallbackData, prefix="time"):
# # #     """Класс для обработки callback_data."""
# # #
# # #     action: str  # up, down, back, select
# # #     target: str  # hour1, hour2, min1, min2
# # #
# # #
# # # class TimePicker:
# # #     """Класс для создания инлайн-клавиатуры выбора времени и обработки колбэков."""
# # #
# # #     def __init__(self):
# # #         self.user_time = {"hour1": 0, "hour2": 0, "min1": 0, "min2": 0}
# # #
# # #     async def create_time_keyboard(self) -> InlineKeyboardMarkup:
# # #         """Создает инлайн-клавиатуру для выбора времени."""
# # #         builder = InlineKeyboardBuilder()
# # #
# # #         # Верхний ряд стрелок
# # #         builder.row(
# # #             InlineKeyboardButton(
# # #                 text="▲", callback_data=TimeCallback(action="up", target="hour1").pack()
# # #             ),
# # #             InlineKeyboardButton(
# # #                 text="▲", callback_data=TimeCallback(action="up", target="hour2").pack()
# # #             ),
# # #             InlineKeyboardButton(text=" ", callback_data="noop"),  # Пустая кнопка
# # #             InlineKeyboardButton(
# # #                 text="▲", callback_data=TimeCallback(action="up", target="min1").pack()
# # #             ),
# # #             InlineKeyboardButton(
# # #                 text="▲", callback_data=TimeCallback(action="up", target="min2").pack()
# # #             ),
# # #         )
# # #
# # #         # Числа с двоеточием
# # #         builder.row(
# # #             InlineKeyboardButton(
# # #                 text=f"{self.user_time['hour1']}", callback_data="noop"
# # #             ),
# # #             InlineKeyboardButton(
# # #                 text=f"{self.user_time['hour2']}", callback_data="noop"
# # #             ),
# # #             InlineKeyboardButton(text=":", callback_data="noop"),
# # #             InlineKeyboardButton(
# # #                 text=f"{self.user_time['min1']}", callback_data="noop"
# # #             ),
# # #             InlineKeyboardButton(
# # #                 text=f"{self.user_time['min2']}", callback_data="noop"
# # #             ),
# # #         )
# # #
# # #         # Нижний ряд стрелок
# # #         builder.row(
# # #             InlineKeyboardButton(
# # #                 text="▼",
# # #                 callback_data=TimeCallback(action="down", target="hour1").pack(),
# # #             ),
# # #             InlineKeyboardButton(
# # #                 text="▼",
# # #                 callback_data=TimeCallback(action="down", target="hour2").pack(),
# # #             ),
# # #             InlineKeyboardButton(text=" ", callback_data="noop"),  # Пустая кнопка
# # #             InlineKeyboardButton(
# # #                 text="▼",
# # #                 callback_data=TimeCallback(action="down", target="min1").pack(),
# # #             ),
# # #             InlineKeyboardButton(
# # #                 text="▼",
# # #                 callback_data=TimeCallback(action="down", target="min2").pack(),
# # #             ),
# # #         )
# # #
# # #         # Кнопки Назад и Выбрать
# # #         builder.row(
# # #             InlineKeyboardButton(
# # #                 text=" ",
# # #                 callback_data=TimeCallback(action=" ", target="none").pack(),
# # #             ),
# # #             InlineKeyboardButton(
# # #                 text="Выбрать",
# # #                 callback_data=TimeCallback(action="select", target="none").pack(),
# # #             ),
# # #         )
# # #
# # #         return builder.as_markup()
# # #
# # #     async def handle_callback(
# # #         self, callback: CallbackQuery, callback_data: TimeCallback
# # #     ):
# # #         """Обрабатывает нажатия на кнопки."""
# # #         # Получение текущего значения
# # #         if callback_data.target != "none":
# # #             current_value = self.user_time[callback_data.target]
# # #
# # #         # Логика изменения значений
# # #         if callback_data.action == "up":
# # #             max_value = (
# # #                 2
# # #                 if callback_data.target == "hour1" and self.user_time["hour2"] > 3
# # #                 else 9
# # #             )
# # #             self.user_time[callback_data.target] = (current_value + 1) % (max_value + 1)
# # #
# # #         elif callback_data.action == "down":
# # #             max_value = (
# # #                 2
# # #                 if callback_data.target == "hour1" and self.user_time["hour2"] > 3
# # #                 else 9
# # #             )
# # #             self.user_time[callback_data.target] = (current_value - 1) % (max_value + 1)
# # #
# # #         # Ограничения времени
# # #         hours = int(f"{self.user_time['hour1']}{self.user_time['hour2']}")
# # #         minutes = int(f"{self.user_time['min1']}{self.user_time['min2']}")
# # #
# # #         if hours > 23:
# # #             self.user_time["hour1"], self.user_time["hour2"] = 2, 3
# # #         if minutes > 59:
# # #             self.user_time["min1"], self.user_time["min2"] = 5, 9
# # #
# # #         # Действие на кнопках
# # #         if callback_data.action == "select":
# # #             selected_time = f"{hours:02}:{minutes:02}"
# # #             # await callback.message.answer(f"Вы выбрали время: {selected_time}")
# # #             print(selected_time)
# # #             return selected_time
# # #         elif callback_data.action == "back":
# # #             print("back")
# # #             # await callback.message.answer("Возвращаемся назад.")
# # #         else:
# # #             # Обновление клавиатуры
# # #             await callback.message.edit_reply_markup(
# # #                 reply_markup=await self.create_time_keyboard()
# # #             )
# # #
# # #         await callback.answer()
# # from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
# # from aiogram.filters.callback_data import CallbackData
# # from aiogram.utils.keyboard import InlineKeyboardBuilder
# #
# #
# # class TimeCallback(CallbackData, prefix="time"):
# #     """Класс для обработки callback_data."""
# #
# #     action: str  # up, down, back, select
# #     target: str  # hour1, hour2, min1, min2
# #
# #
# # class TimePicker:
# #     """Класс для создания инлайн-клавиатуры выбора времени и обработки колбэков."""
# #
# #     def __init__(self):
# #         self.user_time = {"hour1": 0, "hour2": 0, "min1": 0, "min2": 0}
# #
# #     async def create_time_keyboard(self) -> InlineKeyboardMarkup:
# #         """Создает инлайн-клавиатуру для выбора времени."""
# #         builder = InlineKeyboardBuilder()
# #
# #         # Верхний ряд стрелок
# #         builder.row(
# #             InlineKeyboardButton(
# #                 text="▲", callback_data=TimeCallback(action="up", target="hour1").pack()
# #             ),
# #             InlineKeyboardButton(
# #                 text="▲", callback_data=TimeCallback(action="up", target="hour2").pack()
# #             ),
# #             InlineKeyboardButton(text=" ", callback_data="noop"),  # Пустая кнопка
# #             InlineKeyboardButton(
# #                 text="▲", callback_data=TimeCallback(action="up", target="min1").pack()
# #             ),
# #             InlineKeyboardButton(
# #                 text="▲", callback_data=TimeCallback(action="up", target="min2").pack()
# #             ),
# #         )
# #
# #         # Числа с двоеточием
# #         builder.row(
# #             InlineKeyboardButton(
# #                 text=f"{self.user_time['hour1']}", callback_data="noop"
# #             ),
# #             InlineKeyboardButton(
# #                 text=f"{self.user_time['hour2']}", callback_data="noop"
# #             ),
# #             InlineKeyboardButton(text=":", callback_data="noop"),
# #             InlineKeyboardButton(
# #                 text=f"{self.user_time['min1']}", callback_data="noop"
# #             ),
# #             InlineKeyboardButton(
# #                 text=f"{self.user_time['min2']}", callback_data="noop"
# #             ),
# #         )
# #
# #         # Нижний ряд стрелок
# #         builder.row(
# #             InlineKeyboardButton(
# #                 text="▼",
# #                 callback_data=TimeCallback(action="down", target="hour1").pack(),
# #             ),
# #             InlineKeyboardButton(
# #                 text="▼",
# #                 callback_data=TimeCallback(action="down", target="hour2").pack(),
# #             ),
# #             InlineKeyboardButton(text=" ", callback_data="noop"),  # Пустая кнопка
# #             InlineKeyboardButton(
# #                 text="▼",
# #                 callback_data=TimeCallback(action="down", target="min1").pack(),
# #             ),
# #             InlineKeyboardButton(
# #                 text="▼",
# #                 callback_data=TimeCallback(action="down", target="min2").pack(),
# #             ),
# #         )
# #
# #         # Кнопки Назад и Выбрать
# #         builder.row(
# #             InlineKeyboardButton(
# #                 text=" ",
# #                 callback_data=TimeCallback(action=" ", target="none").pack(),
# #             ),
# #             InlineKeyboardButton(
# #                 text="Выбрать",
# #                 callback_data=TimeCallback(action="select", target="none").pack(),
# #             ),
# #         )
# #
# #         return builder.as_markup()
# #
# #     async def handle_callback(
# #         self, callback: CallbackQuery, callback_data: TimeCallback
# #     ):
# #         """Обрабатывает нажатия на кнопки."""
# #         if callback_data.target != "none":
# #             current_value = self.user_time[callback_data.target]
# #
# #         if callback_data.action == "up":
# #             max_value = 9
# #             self.user_time[callback_data.target] = (current_value + 1) % (max_value + 1)
# #
# #         elif callback_data.action == "down":
# #             max_value = 9
# #             self.user_time[callback_data.target] = (current_value - 1) % (max_value + 1)
# #
# #         # Ограничения времени
# #         hours = int(f"{self.user_time['hour1']}{self.user_time['hour2']}")
# #         minutes = int(f"{self.user_time['min1']}{self.user_time['min2']}")
# #
# #         if hours > 23:
# #             self.user_time["hour1"], self.user_time["hour2"] = 2, 3
# #         if minutes > 59:
# #             self.user_time["min1"], self.user_time["min2"] = 5, 9
# #
# #         if callback_data.action == "select":
# #             selected_time = f"{hours:02}:{minutes:02}"
# #             # print(selected_time)
# #             return selected_time
# #         else:
# #             new_keyboard = await self.create_time_keyboard()
# #             if new_keyboard != callback.message.reply_markup:
# #                 await callback.message.edit_reply_markup(reply_markup=new_keyboard)
# #
# #         await callback.answer()
# from aiogram.filters.callback_data import CallbackData
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
# from aiogram.utils.keyboard import InlineKeyboardBuilder
#
#
# # CallbackData для времени
# class TimeCallback(CallbackData, prefix="time"):
#     """CallbackData для выбора времени"""
#
#     action: str  # up, down, back, select
#     target: str  # hour1, hour2, min1, min2
#
#
# # class TimePicker:
# #     """Класс для управления выбором времени."""
# #
# #     def __init__(self):
# #         # Хранилище выбранного времени
# #         self.user_time = {"hour1": 0, "hour2": 0, "min1": 0, "min2": 0}
# #
# #     # Создание клавиатуры
# #     async def create_time_keyboard(self) -> InlineKeyboardMarkup:
# #         builder = InlineKeyboardBuilder()
# #
# #         # Верхний ряд стрелок
# #         builder.row(
# #             InlineKeyboardButton(
# #                 text="▲", callback_data=TimeCallback(action="up", target="hour1").pack()
# #             ),
# #             InlineKeyboardButton(
# #                 text="▲", callback_data=TimeCallback(action="up", target="hour2").pack()
# #             ),
# #             InlineKeyboardButton(text=" ", callback_data="noop"),  # Пустая кнопка
# #             InlineKeyboardButton(
# #                 text="▲", callback_data=TimeCallback(action="up", target="min1").pack()
# #             ),
# #             InlineKeyboardButton(
# #                 text="▲", callback_data=TimeCallback(action="up", target="min2").pack()
# #             ),
# #         )
# #
# #         # Числа с двоеточием
# #         builder.row(
# #             InlineKeyboardButton(
# #                 text=f"{self.user_time['hour1']}", callback_data="noop"
# #             ),
# #             InlineKeyboardButton(
# #                 text=f"{self.user_time['hour2']}", callback_data="noop"
# #             ),
# #             InlineKeyboardButton(text=":", callback_data="noop"),
# #             InlineKeyboardButton(
# #                 text=f"{self.user_time['min1']}", callback_data="noop"
# #             ),
# #             InlineKeyboardButton(
# #                 text=f"{self.user_time['min2']}", callback_data="noop"
# #             ),
# #         )
# #
# #         # Нижний ряд стрелок
# #         builder.row(
# #             InlineKeyboardButton(
# #                 text="▼",
# #                 callback_data=TimeCallback(action="down", target="hour1").pack(),
# #             ),
# #             InlineKeyboardButton(
# #                 text="▼",
# #                 callback_data=TimeCallback(action="down", target="hour2").pack(),
# #             ),
# #             InlineKeyboardButton(text=" ", callback_data="noop"),  # Пустая кнопка
# #             InlineKeyboardButton(
# #                 text="▼",
# #                 callback_data=TimeCallback(action="down", target="min1").pack(),
# #             ),
# #             InlineKeyboardButton(
# #                 text="▼",
# #                 callback_data=TimeCallback(action="down", target="min2").pack(),
# #             ),
# #         )
# #
# #         # Кнопки Назад и Выбрать
# #         builder.row(
# #             InlineKeyboardButton(
# #                 text="Назад",
# #                 callback_data=TimeCallback(action="back", target="none").pack(),
# #             ),
# #             InlineKeyboardButton(
# #                 text="Выбрать",
# #                 callback_data=TimeCallback(action="select", target="none").pack(),
# #             ),
# #         )
# #
# #         return builder.as_markup()
# #
# #     # Обработчик колбэков
# #     async def handle_time_callback(
# #         self, callback: CallbackQuery, callback_data: TimeCallback
# #     ):
# #         # Получение текущего значения
# #         if callback_data.target != "none":
# #             current_value = self.user_time[callback_data.target]
# #
# #         # Логика изменения значений
# #         if callback_data.action == "up":
# #             if callback_data.target.startswith("hour"):
# #                 max_value = (
# #                     2
# #                     if callback_data.target == "hour1" and self.user_time["hour2"] > 3
# #                     else 9
# #                 )
# #             else:
# #                 max_value = 9
# #             self.user_time[callback_data.target] = (current_value + 1) % (max_value + 1)
# #
# #         elif callback_data.action == "down":
# #             if callback_data.target.startswith("hour"):
# #                 max_value = (
# #                     2
# #                     if callback_data.target == "hour1" and self.user_time["hour2"] > 3
# #                     else 9
# #                 )
# #             else:
# #                 max_value = 9
# #             self.user_time[callback_data.target] = (current_value - 1) % (max_value + 1)
# #
# #         # Ограничения времени
# #         hours = int(f"{self.user_time['hour1']}{self.user_time['hour2']}")
# #         minutes = int(f"{self.user_time['min1']}{self.user_time['min2']}")
# #
# #         if hours > 23:
# #             self.user_time["hour1"], self.user_time["hour2"] = 2, 3
# #         if minutes > 59:
# #             self.user_time["min1"], self.user_time["min2"] = 5, 9
# #
# #         # Действие на кнопках
# #         if callback_data.action == "select":
# #             selected_time = f"{hours:02}:{minutes:02}"
# #             # await callback.message.answer(f"Вы выбрали время: {selected_time}")
# #             return selected_time
# #         elif callback_data.action == "back":
# #             # await callback.message.answer("Возвращаемся назад.")
# #             print("back")
# #         else:
# #             # Обновление клавиатуры
# #             await callback.message.edit_reply_markup(
# #                 reply_markup=await self.create_time_keyboard()
# #             )
# #
# #         await callback.answer()
# class TimePicker:
#     """Класс для управления выбором времени."""
#
#     def __init__(self, initial_time=None):
#         """
#         Конструктор, который принимает начальное время, если оно передано.
#         """
#         # Если начальное время передано, то используем его, иначе задаём по умолчанию.
#         if initial_time:
#             hours, minutes = map(int, initial_time.split(":"))
#             self.user_time = {
#                 "hour1": hours // 10,
#                 "hour2": hours % 10,
#                 "min1": minutes // 10,
#                 "min2": minutes % 10,
#             }
#         else:
#             self.user_time = {"hour1": 0, "hour2": 0, "min1": 0, "min2": 0}
#
#     # Создание клавиатуры (без изменений)
#     async def create_time_keyboard(self) -> InlineKeyboardMarkup:
#         builder = InlineKeyboardBuilder()
#
#         # Верхний ряд стрелок
#         builder.row(
#             InlineKeyboardButton(
#                 text="▲", callback_data=TimeCallback(action="up", target="hour1").pack()
#             ),
#             InlineKeyboardButton(
#                 text="▲", callback_data=TimeCallback(action="up", target="hour2").pack()
#             ),
#             InlineKeyboardButton(text=" ", callback_data="noop"),  # Пустая кнопка
#             InlineKeyboardButton(
#                 text="▲", callback_data=TimeCallback(action="up", target="min1").pack()
#             ),
#             InlineKeyboardButton(
#                 text="▲", callback_data=TimeCallback(action="up", target="min2").pack()
#             ),
#         )
#
#         # Числа с двоеточием
#         builder.row(
#             InlineKeyboardButton(
#                 text=f"{self.user_time['hour1']}", callback_data="noop"
#             ),
#             InlineKeyboardButton(
#                 text=f"{self.user_time['hour2']}", callback_data="noop"
#             ),
#             InlineKeyboardButton(text=":", callback_data="noop"),
#             InlineKeyboardButton(
#                 text=f"{self.user_time['min1']}", callback_data="noop"
#             ),
#             InlineKeyboardButton(
#                 text=f"{self.user_time['min2']}", callback_data="noop"
#             ),
#         )
#
#         # Нижний ряд стрелок
#         builder.row(
#             InlineKeyboardButton(
#                 text="▼",
#                 callback_data=TimeCallback(action="down", target="hour1").pack(),
#             ),
#             InlineKeyboardButton(
#                 text="▼",
#                 callback_data=TimeCallback(action="down", target="hour2").pack(),
#             ),
#             InlineKeyboardButton(text=" ", callback_data="noop"),  # Пустая кнопка
#             InlineKeyboardButton(
#                 text="▼",
#                 callback_data=TimeCallback(action="down", target="min1").pack(),
#             ),
#             InlineKeyboardButton(
#                 text="▼",
#                 callback_data=TimeCallback(action="down", target="min2").pack(),
#             ),
#         )
#
#         # Кнопки Назад и Выбрать
#         builder.row(
#             InlineKeyboardButton(
#                 text="Назад",
#                 callback_data=TimeCallback(action="back", target="none").pack(),
#             ),
#             InlineKeyboardButton(
#                 text="Выбрать",
#                 callback_data=TimeCallback(action="select", target="none").pack(),
#             ),
#         )
#
#         return builder.as_markup()
#
#     # Обработчик колбэков (без изменений)
#     async def handle_time_callback(
#         self, callback: CallbackQuery, callback_data: TimeCallback
#     ):
#         if callback_data.target != "none":
#             current_value = self.user_time[callback_data.target]
#
#         if callback_data.action == "up":
#             if callback_data.target.startswith("hour"):
#                 max_value = (
#                     2
#                     if callback_data.target == "hour1" and self.user_time["hour2"] > 3
#                     else 9
#                 )
#             else:
#                 max_value = 9
#             self.user_time[callback_data.target] = (current_value + 1) % (max_value + 1)
#
#         elif callback_data.action == "down":
#             if callback_data.target.startswith("hour"):
#                 max_value = (
#                     2
#                     if callback_data.target == "hour1" and self.user_time["hour2"] > 3
#                     else 9
#                 )
#             else:
#                 max_value = 9
#             self.user_time[callback_data.target] = (current_value - 1) % (max_value + 1)
#
#         hours = int(f"{self.user_time['hour1']}{self.user_time['hour2']}")
#         minutes = int(f"{self.user_time['min1']}{self.user_time['min2']}")
#
#         if hours > 23:
#             self.user_time["hour1"], self.user_time["hour2"] = 2, 3
#         if minutes > 59:
#             self.user_time["min1"], self.user_time["min2"] = 5, 9
#
#         if callback_data.action == "select":
#             selected_time = f"{hours:02}:{minutes:02}"
#             return selected_time
#         elif callback_data.action == "back":
#             print("back")
#         else:
#             await callback.message.edit_reply_markup(
#                 reply_markup=await self.create_time_keyboard()
#             )
#
#         await callback.answer()
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters.callback_data import CallbackData


class TimeCallback(CallbackData, prefix="time"):
    """CallbackData для выбора времени."""

    action: str  # Действие: "up", "down", "select", "back"
    target: str  # Цель: hour1, hour2, min1, min2


class TimePicker:
    """Класс для управления выбором времени."""

    def __init__(self, initial_time=None):
        """
        Конструктор, который принимает начальное время, если оно передано.
        """
        if initial_time:
            hours, minutes = map(int, initial_time.split(":"))
            self.user_time = {
                "hour1": hours // 10,
                "hour2": hours % 10,
                "min1": minutes // 10,
                "min2": minutes % 10,
            }
        else:
            self.user_time = {"hour1": 0, "hour2": 0, "min1": 0, "min2": 0}

    async def create_time_keyboard(self, l10n) -> InlineKeyboardMarkup:
        """Создает инлайн-клавиатуру для выбора времени."""
        builder = InlineKeyboardMarkup(inline_keyboard=[])

        # Верхний ряд стрелок
        builder.inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text="▲",
                    callback_data=TimeCallback(action="up", target="hour1").pack(),
                ),
                InlineKeyboardButton(
                    text="▲",
                    callback_data=TimeCallback(action="up", target="hour2").pack(),
                ),
                InlineKeyboardButton(text=" ", callback_data="noop"),
                InlineKeyboardButton(
                    text="▲",
                    callback_data=TimeCallback(action="up", target="min1").pack(),
                ),
                InlineKeyboardButton(
                    text="▲",
                    callback_data=TimeCallback(action="up", target="min2").pack(),
                ),
            ]
        )

        # Числа с двоеточием
        builder.inline_keyboard.append(
            [
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
            ]
        )

        # Нижний ряд стрелок
        builder.inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text="▼",
                    callback_data=TimeCallback(action="down", target="hour1").pack(),
                ),
                InlineKeyboardButton(
                    text="▼",
                    callback_data=TimeCallback(action="down", target="hour2").pack(),
                ),
                InlineKeyboardButton(text=" ", callback_data="noop"),
                InlineKeyboardButton(
                    text="▼",
                    callback_data=TimeCallback(action="down", target="min1").pack(),
                ),
                InlineKeyboardButton(
                    text="▼",
                    callback_data=TimeCallback(action="down", target="min2").pack(),
                ),
            ]
        )

        # Кнопки Назад и Выбрать
        builder.inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text=" ",
                    callback_data=TimeCallback(action="back", target="none").pack(),
                ),
                InlineKeyboardButton(
                    text=l10n.format_value("select_time"),
                    callback_data=TimeCallback(action="select", target="none").pack(),
                ),
            ]
        )

        return builder

    async def handle_time_callback(
        self, callback: CallbackQuery, callback_data: TimeCallback, l10n
    ):
        """Обрабатывает колбэк от кнопок выбора времени."""
        if callback_data.target != "none":
            # Получаем текущую цифру
            current_value = self.user_time[callback_data.target]

            if callback_data.action == "up":
                # Увеличиваем цифру на 1, с переходом через 9
                self.user_time[callback_data.target] = (current_value + 1) % 10
            elif callback_data.action == "down":
                # Уменьшаем цифру на 1, с переходом через 0
                self.user_time[callback_data.target] = (current_value - 1) % 10

        if callback_data.action == "select":

            # Формируем выбранное время
            selected_time = f"{self.user_time['hour1']}{self.user_time['hour2']}:{self.user_time['min1']}{self.user_time['min2']}"
            return selected_time  # Возвращаем время для проверки в другом месте

        # Обновляем клавиатуру
        await callback.message.edit_reply_markup(
            reply_markup=await self.create_time_keyboard(l10n)
        )
        await callback.answer()
