import enum

from sqlalchemy import Column, Integer, String, Enum, JSON, ForeignKey, Boolean

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

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
    ARCHIVED = "archived"


class Contest(Base):
    __tablename__ = "contests"

    id = Column(
        Integer, primary_key=True, autoincrement=True
    )  # Уникальный идентификатор
    user_id = Column(Integer, nullable=False)  # Идентификатор пользователя
    message_id = Column(String, nullable=False)  # Идентификатор сообщения
    channel_id = Column(String, nullable=False)  # Идентификатор канала
    channel_name = Column(String, nullable=True)  # Имя канала
    descripbtion = Column(String, nullable=True)  # Текст сообщения
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


class ContestParticipant(Base):
    __tablename__ = "contest_participants"

    id = Column(
        Integer, primary_key=True, autoincrement=True
    )  # Уникальный идентификатор
    contest_id = Column(
        Integer, ForeignKey("contests.id"), nullable=False
    )  # ID конкурса
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # ID пользователя
    participation_time = Column(String, nullable=False)  # Время участия
    winner = Column(Boolean, default=False)  # Флаг победителя

    # Связи
    contest = relationship("Contest", backref="participants")  # Связь с конкурсом
    user = relationship("User", backref="participations")  # Связь с пользователем


class ContestLog(Base):
    __tablename__ = "contest_logs"

    id = Column(
        Integer, primary_key=True, autoincrement=True
    )  # Уникальный идентификатор
    contest_id = Column(
        Integer, ForeignKey("contests.id"), nullable=False
    )  # ID конкурса
    action = Column(
        String, nullable=False
    )  # Действие (например, "создан", "обновлен", "победители определены")
    timestamp = Column(String, nullable=False)  # Время действия
    user_id = Column(
        Integer, ForeignKey("users.id"), nullable=True
    )  # Кто выполнил действие (может быть NULL)

    # Связь с конкурсом
    contest = relationship("Contest", backref="logs")


class ChannelSubscription(Base):
    __tablename__ = "channel_subscriptions"

    id = Column(
        Integer, primary_key=True, autoincrement=True
    )  # Уникальный идентификатор
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # ID пользователя
    channel_id = Column(String, nullable=False)  # ID канала
    subscribed_at = Column(String, nullable=False)  # Время подписки
    unsubscribed_at = Column(
        String, nullable=True
    )  # Время отписки (NULL, если не отписан)

    # Связь с пользователем
    user = relationship("User", backref="subscriptions")


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
