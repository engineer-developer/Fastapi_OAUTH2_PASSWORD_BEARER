from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.models import User


async def fetch_all_users(session: AsyncSession) -> Sequence[User]:
    """Fetch all users"""

    stmt = select(User)
    result = await session.execute(stmt)
    users = result.scalars().all()

    return users


async def fetch_user_by_id(session: AsyncSession, id: int) -> User:
    """Fetch user by id"""

    stmt = select(User).where(User.id == id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    return user
