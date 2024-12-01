from asyncio import current_task
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from src.config.config import settings

engine = create_async_engine(url=settings.db.url, echo=True)

async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
    class_=AsyncSession,
)

scoped_session = async_scoped_session(
    session_factory=async_session,
    scopefunc=current_task,
)


async def get_session():
    async with async_session() as session:
        yield session


async def get_scoped_session():
    async with scoped_session() as session:
        yield session


async def get_engine() -> AsyncConnection:
    async with engine.begin() as connection:
        yield connection


CommonAsyncSession = Annotated[AsyncSession, Depends(get_session)]
CommonAsyncScopedSession = Annotated[AsyncSession, Depends(get_scoped_session)]
CommonAsyncEngine = Annotated[AsyncConnection, Depends(get_engine)]
