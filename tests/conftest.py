import shutil
from pathlib import Path
from typing import AsyncGenerator

import pytest
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from httpx import AsyncClient, ASGITransport

from src.database.database import get_session
from src.dao.base_model import metadata
from src.dao.models import User
from src.config.config import settings
from src.core.fastapi_factory import create_app


db_url = settings.db.url
print(f"\n{'*'*70}\n{db_url=}\n{'*'*70}\n")


engine_test = create_async_engine(
    url=db_url,
    poolclass=NullPool,
    echo=True,
)
async_session = async_sessionmaker(
    engine_test, class_=AsyncSession, expire_on_commit=False
)
metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)


@pytest.fixture(scope="session")
def app():
    _app = create_app()
    _app.dependency_overrides[get_session] = override_get_async_session
    yield _app


@pytest.fixture(scope="session")
async def async_client(app) -> AsyncGenerator[AsyncClient, None]:
    """Create async client"""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as async_client:
        yield async_client
