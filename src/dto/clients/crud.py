from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import ORJSONResponse
from pydantic import ValidationError, Field

from src.auth.basic_auth import check_token, oauth2_scheme
from src.dao.models import Password, Client
from src.database.database import CommonAsyncSession
from src.dto.clients.schemas import ClientOutSchema, ClientCreateSchema, ClientNotFound
from src.dto.clients.utils import fetch_all_clients, fetch_client_by_id
from src.dto.passwords.utils import create_hashed_password


router = APIRouter(
    prefix="/clients",
    tags=["Clients"],
)


@router.get(
    "/",
    response_model=list[ClientOutSchema],
    responses={
        404: {
            "description": "Clients not found",
            "model": ClientNotFound,
        },
    },
)
async def get_all_clients(
    session: CommonAsyncSession,
):
    """Get all clients from database"""

    clients_orm = await fetch_all_clients(session)

    if not clients_orm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Clients not found",
        )
    return clients_orm


@router.post("/", response_model=ClientOutSchema, status_code=201)
async def add_new_client(
    session: CommonAsyncSession,
    client: ClientCreateSchema,
):
    """Add new client to database"""
    async with session.begin():
        new_password_orm: Password = await create_hashed_password(
            session,
            client.password,
        )
        session.add(new_password_orm)
        await session.flush()
        new_client_orm = Client(**client.model_dump(exclude={"password"}))
        new_client_orm.password_id = new_password_orm.id
        session.add(new_client_orm)

    return new_client_orm


@router.delete("/{client_id}", response_class=ORJSONResponse)
async def delete_client(
    session: CommonAsyncSession,
    client_id: int,
):
    """Delete client from database"""
    client = await fetch_client_by_id(session, client_id)
    await session.delete(client)

    return {"deleted": "True"}


@router.post("/{client_id}", response_model=ClientOutSchema)
async def get_client_by_password(
    session: CommonAsyncSession,
    client_id: int,
    token: Annotated[str, Depends(oauth2_scheme)],
):
    """Delete client from database"""
    print(f"{token=}")

    client = await fetch_client_by_id(session, client_id)

    return client
