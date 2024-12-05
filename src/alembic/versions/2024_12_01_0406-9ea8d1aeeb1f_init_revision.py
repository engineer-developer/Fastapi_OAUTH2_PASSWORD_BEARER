"""Init revision

Revision ID: 9ea8d1aeeb1f
Revises:
Create Date: 2024-12-01 04:06:38.507551

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9ea8d1aeeb1f"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    passwords_table = op.create_table(
        "passwords",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("salt", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_passwords")),
    )
    users_table = op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column(
            "role",
            sa.Enum("admin", "client", name="role"),
            nullable=False,
        ),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("password_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["password_id"],
            ["passwords.id"],
            name=op.f("fk_users_password_id_passwords"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
        sa.UniqueConstraint("email", name=op.f("uq_users_email_")),
        sa.UniqueConstraint("password_id", name=op.f("uq_users_password_id_")),
    )

    def insert_value_in_table(table: TableClause, value: dict):
        op.bulk_insert(table, [value, ])

    password_value = {
        "hashed_password": "bf91848c83fd4bd1928ed18083b441064e7918a4275c6aaf7f9865ef4c7bde2c67692b5a4f207abe0820fc1c91a3824938d1d265e9d3943ac89a9e9abe923327",
        "salt": "ecb91d1e2b644bf3812ec7de603c10e5"
    }
    user_value = {
        "username": "some_user",
        "email": "user@example.com",
        "role": "admin",
        "is_active": True,
        "password_id": 1
    }
    insert_value_in_table(passwords_table, password_value)
    insert_value_in_table(users_table, user_value)


def downgrade() -> None:
    op.drop_table("users")
    op.drop_table("passwords")
    op.execute("DROP TYPE role;")
