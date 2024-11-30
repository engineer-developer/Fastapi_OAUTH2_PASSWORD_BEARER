from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import ORJSONResponse
from pydantic import ValidationError, Field

from src.auth.basic_auth import check_token, oauth2_scheme
from src.dao.models import Password, User
from src.database.database import CommonAsyncSession
from src.dto.users.schemas import UserOutSchema, UserCreateSchema, UserNotFound
from src.dto.users.utils import fetch_all_users, fetch_user_by_id
from src.dto.passwords.utils import create_hashed_password


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "/",
    response_model=list[UserOutSchema],
    responses={
        404: {
            "description": "Users not found",
            "model": UserNotFound,
        },
    },
)
async def get_all_users(
    session: CommonAsyncSession,
):
    """Get all users from database"""

    users_orm = await fetch_all_users(session)

    if not users_orm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Users not found",
        )
    return users_orm


@router.post("/", response_model=UserOutSchema, status_code=201)
async def add_new_user(
    session: CommonAsyncSession,
    user: UserCreateSchema,
):
    """Add new user to database"""
    async with session.begin():
        new_password_orm: Password = await create_hashed_password(
            session,
            user.password,
        )
        session.add(new_password_orm)
        await session.flush()
        new_user_orm = User(**user.model_dump(exclude={"password"}))
        new_user_orm.password_id = new_password_orm.id
        session.add(new_user_orm)

    return new_user_orm


@router.delete("/{user_id}", response_class=ORJSONResponse)
async def delete_user(
    session: CommonAsyncSession,
    user_id: int,
):
    """Delete user from database"""
    user = await fetch_user_by_id(session, user_id)
    await session.delete(user)

    return {"deleted": "True"}


@router.post("/{user_id}", response_model=UserOutSchema)
async def get_user_by_password(
    session: CommonAsyncSession,
    user_id: int,
    token: Annotated[str, Depends(oauth2_scheme)],
):
    """Delete user from database"""
    print(f"{token=}")

    user = await fetch_user_by_id(session, user_id)

    return user
