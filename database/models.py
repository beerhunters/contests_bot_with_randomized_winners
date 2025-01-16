import enum

from sqlalchemy import Column, Integer, String, Enum, JSON

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


DATABASE_URL = "sqlite+aiosqlite:///db.sqlite3"

engine = create_async_engine(url=DATABASE_URL, echo=True, future=True)

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, nullable=True)
    full_name = Column(String, nullable=True)
    language_code = Column(String, default="ru")


class ContestStatus(enum.Enum):
    DRAFT = "draft"  # Неопубликованный
    PUBLISHED = "published"  # Опубликованный
    FINISHED = "finished"  # Завершенный


class Contest(Base):
    __tablename__ = "contests"

    id = Column(
        Integer, primary_key=True, autoincrement=True
    )  # Уникальный идентификатор
    user_id = Column(Integer, nullable=False)  # Идентификатор пользователя
    message_id = Column(String, nullable=False)  # Идентификатор сообщения
    channel_id = Column(String, nullable=False)  # Идентификатор канала
    channel_name = Column(String, nullable=True)  # Имя канала
    text = Column(String, nullable=True)  # Текст сообщения
    file_type = Column(String, nullable=True)  # Тип файла
    file_id = Column(String, nullable=True)  # Идентификатор файла
    winners_count = Column(Integer, nullable=False)  # Количество победителей
    post_time = Column(String, nullable=False)  # Время публикации
    end_time = Column(String, nullable=False)  # Время завершения розыгрыша
    status = Column(
        Enum(ContestStatus), default=ContestStatus.DRAFT
    )  # Статус розыгрыша
    required_channels = Column(
        JSON, nullable=True
    )  # Список обязательных каналов для подписки
    prizes = Column(JSON, nullable=True)  # Список призов
    location = Column(JSON, nullable=True)  # Геолокация розыгрыша


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
