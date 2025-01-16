from functools import wraps

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User, async_session


def db_session(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            return await func(*args, **kwargs, db=session)

    return wrapper


@db_session
async def get_user_by_tg_id(tg_id: int, db: AsyncSession):
    query = select(User).filter(User.tg_id == tg_id)
    result = await db.execute(query)
    return result.scalars().first()


@db_session
async def add_user_to_db(
    tg_id: int, username: str, full_name: str, language_code: str, db: AsyncSession
):
    user = User(
        tg_id=tg_id, username=username, full_name=full_name, language_code=language_code
    )
    db.add(user)
    await db.commit()
