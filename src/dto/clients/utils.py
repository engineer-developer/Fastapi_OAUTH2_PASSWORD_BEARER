from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.models import Client


async def fetch_all_clients(session: AsyncSession) -> Sequence[Client]:
    """Fetch all clients"""

    stmt = select(Client)
    result = await session.execute(stmt)
    clients = result.scalars().all()

    return clients


async def fetch_client_by_id(session: AsyncSession, id: int) -> Client:
    """Fetch client by id"""

    stmt = select(Client).where(Client.id == id)
    result = await session.execute(stmt)
    client = result.scalar_one_or_none()

    return client
