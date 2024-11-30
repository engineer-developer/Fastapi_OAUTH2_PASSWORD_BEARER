from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBaseSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    name: Optional[str]
    email: EmailStr


class UserCreateSchema(UserBaseSchema):
    password: str = Field(min_length=10)


class UserOutSchema(UserBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int


class UserNotFound(BaseModel):
    detail: str = "Users not found"
