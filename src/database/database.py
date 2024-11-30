from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    AsyncConnection,
)
from fastapi import Depends
from typing import Annotated

from config.config import settings


engine = create_async_engine(url=settings.db.url, echo=True)

async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
    class_=AsyncSession,
)


async def get_session():
    async with async_session() as session:
        yield session


async def get_engine() -> AsyncConnection:
    async with engine.begin() as connection:
        yield connection


CommonAsyncSession = Annotated[AsyncSession, Depends(get_session)]
CommonAsyncEngine = Annotated[AsyncConnection, Depends(get_engine)]
