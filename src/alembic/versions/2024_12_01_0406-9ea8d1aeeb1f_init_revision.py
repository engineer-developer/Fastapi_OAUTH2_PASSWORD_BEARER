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
    op.create_table(
        "passwords",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("salt", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_passwords")),
    )
    op.create_table(
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


def downgrade() -> None:
    op.drop_table("users")
    op.drop_table("passwords")
    op.execute(sqltext="DROP TYPE role;")
