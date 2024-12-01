import enum
from typing import Optional

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_model import DatabaseModel


class Password(DatabaseModel):
    """Passwords table"""

    __tablename__ = "passwords"

    id: Mapped[int] = mapped_column(primary_key=True)
    hashed_password: Mapped[str]
    salt: Mapped[str]

    user: Mapped["User"] = relationship(
        back_populates="password",
        cascade="all, delete-orphan",
        uselist=False,
    )


class Role(enum.Enum):
    admin = "admin"
    client = "client"


class User(DatabaseModel):
    """Users table"""

    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("password_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[Optional[str]] = None
    email: Mapped[str] = mapped_column(unique=True)
    role: Mapped[Role]
    is_active: Mapped[bool] = mapped_column(default=True)
    password_id: Mapped[int] = mapped_column(
        ForeignKey(
            "passwords.id",
            ondelete="CASCADE",
        )
    )

    password: Mapped["Password"] = relationship(
        back_populates="user",
        single_parent=True,
        cascade="all, delete-orphan",
        uselist=False,
        lazy="selectin",
    )
