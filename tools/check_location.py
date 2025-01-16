from aiogram import types
from aiogram.fsm.context import FSMContext
from geopy.distance import geodesic

from handlers.contest import contest_router


@contest_router.message(types.ContentType.LOCATION)
async def check_user_location(message: types.Message, state: FSMContext):
    """
    Проверяет, находится ли пользователь в радиусе допустимой зоны розыгрыша.
    """
    user_location = message.location
    user_coords = (user_location.latitude, user_location.longitude)

    # Получаем данные о локации розыгрыша из базы или FSM
    contest_location = await state.get_data()
    contest_coords = (contest_location["latitude"], contest_location["longitude"])
    radius_km = contest_location.get("radius_km", 2)  # Радиус по умолчанию 2 км

    # Вычисляем расстояние между точками
    distance_km = geodesic(user_coords, contest_coords).km

    if distance_km <= radius_km:
        await message.answer(
            f"Вы находитесь в пределах {radius_km} км от места розыгрыша! 🎉"
        )
    else:
        await message.answer(
            f"К сожалению, вы находитесь за пределами {radius_km} км от места розыгрыша. "
            f"Расстояние: {distance_km:.2f} км."
        )
