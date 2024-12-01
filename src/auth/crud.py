from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.dto.passwords.utils import is_correct_password
from src.dto.users.utils import fetch_user_by_email
from src.database.database import CommonAsyncScopedSession


router = APIRouter(tags=["Auth"])


@router.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: CommonAsyncScopedSession,
) -> dict[str, str]:
    """Get credentials from form-data"""

    given_email = form_data.username
    given_password = form_data.password

    user = await fetch_user_by_email(session, given_email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )

    password_is_valid = await is_correct_password(
        session=session,
        hashed_pw=user.password.hashed_password,
        salt=user.password.salt,
        password=given_password,
    )

    if not password_is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )

    return {"access_token": user.email, "token_type": "bearer"}
