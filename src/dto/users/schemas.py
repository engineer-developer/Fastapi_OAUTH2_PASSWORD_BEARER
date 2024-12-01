import enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class Role(str, enum.Enum):
    admin = "admin"
    client = "client"


class UserBaseSchema(BaseModel):
    username: Optional[str]
    email: EmailStr
    role: Role = Field(default=Role.client)


class UserCreateSchema(UserBaseSchema):
    password: str = Field(min_length=10)


class UserUpdateSchema(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[Role] = None
    is_active: Optional[bool] = None


class UserOutSchema(UserBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int


class UserNotFound(BaseModel):
    detail: str = "Users not found"
