from typing import Sequence, Annotated, Optional

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.auth.oauth2_password_bearer.schemas import oauth2_scheme
from src.dao.models import User
from src.database.database import CommonAsyncScopedSession


async def fetch_all_users(session: AsyncSession) -> Sequence[User]:
    """Fetch all users from database"""

    stmt = select(User).order_by(User.id)
    result = await session.execute(stmt)
    users = result.scalars().all()

    return users


async def fetch_user_by_id(session: AsyncSession, id: int) -> Optional[User]:
    """Fetch user by id from database"""

    stmt = select(User).where(User.id == id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    return user


async def fetch_user_by_email(
    session: AsyncSession,
    email: str,
) -> User:
    """Fetch user by email from database"""

    stmt = select(User).where(User.email == email)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    return user


async def get_current_user(
    session: CommonAsyncScopedSession,
    token: Annotated[str, Depends(oauth2_scheme)],
):
    """Get current login user"""

    user = await fetch_user_by_email(session, token)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Get current active login user"""

    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user
