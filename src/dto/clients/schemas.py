from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ClientBaseSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    name: Optional[str]
    email: EmailStr


class ClientCreateSchema(ClientBaseSchema):
    password: str = Field(min_length=10)


class ClientOutSchema(ClientBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int


class ClientNotFound(BaseModel):
    detail: str = "Clients not found"
