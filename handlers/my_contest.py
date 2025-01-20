from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

my_contest_router = Router()


@my_contest_router.message(F.text.in_({"🎉 Мои розыгрыши", "🎉 My giveaways"}))
async def handle_my_contests(message: Message, state: FSMContext):
    """
    Обрабатывает команду "/my_contests".
    """
    await message.answer("В разработке", show_alert=True)
