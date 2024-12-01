import hashlib
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.models import Password
from src.dto.passwords.schemas import PasswordCreateSchema


async def make_hashed_password(
    session: AsyncSession,
    password: str,
    salt: str | None = None,
) -> tuple[str, str]:
    """Make hashed password from given password"""

    if not salt:
        salt = uuid.uuid4().hex
    mix = (password + salt).encode()
    hashed_password = hashlib.sha512(mix).hexdigest()
    return hashed_password, salt


async def is_correct_password(
    session: AsyncSession,
    hashed_pw: str,
    salt: str,
    password: str,
) -> bool:
    """Check equality given password with hashed password"""

    result = await make_hashed_password(session, password, salt)
    return hashed_pw == result[0]


async def create_hashed_password(
    session: AsyncSession,
    password: str,
) -> Password:
    """Create instance of Password"""

    hashed_password, salt = await make_hashed_password(session, password=password)

    new_password_schema = PasswordCreateSchema(
        hashed_password=hashed_password,
        salt=salt,
    )
    new_password_orm = Password(**new_password_schema.model_dump())
    return new_password_orm
