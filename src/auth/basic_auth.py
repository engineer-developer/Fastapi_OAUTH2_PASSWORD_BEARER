from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.http import (
    HTTPBase,
    HTTPAuthorizationCredentials,
    HTTPBasicCredentials,
)
from starlette import status

from src.database.database import CommonAsyncSession


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def check_token(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: CommonAsyncSession,
):
    if token:
        return token
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not auth")
