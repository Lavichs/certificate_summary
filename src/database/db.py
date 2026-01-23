import datetime
import uuid

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy import create_engine
from typing import Annotated
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Mapped, mapped_column
from sqlalchemy import text

from config import settings

engine = create_async_engine(settings.DB_URL_ASYNC)
# engine_sync = create_engine(settings.DB_URL_SYNC)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
# Session = sessionmaker(bind=engine_sync)

uidpk = Annotated[uuid.UUID, mapped_column(primary_key=True)]
created_at = Annotated[
    datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))
]
updated_at = Annotated[
    datetime.datetime,
    mapped_column(
        server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.datetime.utcnow
    ),
]
is_delete = Annotated[bool, mapped_column(nullable=False, default=False)]


# ------------------------------------------------
# Models


class BaseOrmModel(DeclarativeBase):
    pass


class User(BaseOrmModel):
    __tablename__ = "user"

    id: Mapped[uidpk]
    username: Mapped[str]
    isAdmin: Mapped[bool]


class Certificate(BaseOrmModel):
    __tablename__ = "certificate"

    id: Mapped[uidpk]
    cert_center: Mapped[str | None]
    fio: Mapped[str | None]
    post: Mapped[str | None]
    organization: Mapped[str | None]
    expire_date: Mapped[datetime.datetime | None]
    status: Mapped[str | None]
    comment: Mapped[str | None]

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    is_delete: Mapped[is_delete]


# ------------------------------------------------
# Util functions


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(BaseOrmModel.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(BaseOrmModel.metadata.drop_all)


async def get_async_session():
    async with async_session_maker() as session:
        yield session
