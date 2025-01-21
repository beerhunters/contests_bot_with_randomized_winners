import html

from aiogram.enums import ParseMode

from tools.scheduler import scheduler
import keyboards.keyboards as kb


async def save_contest_to_db(data: dict) -> int:
    """Сохраняет данные конкурса в базу данных и возвращает ID записи."""
    # Здесь добавьте свою логику сохранения данных в БД
    contest_id = 1  # Пример ID записи
    return contest_id


async def format_contest_message(data: dict, l10n) -> str:
    """Форматирует сообщение для конкурса."""
    contest_message = f"{l10n.format_value('contest_title')}\n"
    contest_message += f"{l10n.format_value('contest_description')} {html.escape(data['contest_text'])}\n"
    contest_message += f"{l10n.format_value('contest_end_time')} {data['end_time'].strftime('%d.%m.%Y %H:%M')}\n"
    return contest_message


async def send_contest_post(bot, channel_id: int, data: dict, l10n):
    """Отправляет пост в канал с учетом наличия медиа."""
    # Используем функцию для форматирования сообщения
    text = await format_contest_message(data, l10n)

    # Проверяем наличие медиа и отправляем соответствующее сообщение
    media = data.get("file_id")
    if media is not None:
        await bot.send_photo(
            chat_id=channel_id,
            photo=media,
            caption=text,
            parse_mode=ParseMode.HTML,
            reply_markup=await kb.participation(l10n),
        )
    else:
        await bot.send_message(
            chat_id=channel_id,
            text=text,
            parse_mode=ParseMode.HTML,
            reply_markup=await kb.participation(l10n),
        )


async def schedule_contest_post(bot, channel_id: int, data: dict, l10n):
    """Планирует отправку сообщения через APScheduler."""
    post_time = data["post_time"]

    async def post_task():
        await send_contest_post(bot, channel_id, data, l10n)

    scheduler.add_job(post_task, "date", run_date=post_time)
