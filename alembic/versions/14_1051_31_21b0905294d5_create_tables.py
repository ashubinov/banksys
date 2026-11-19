"""create tables

Revision ID: 21b0905294d5
Revises:
Create Date: 2026-05-14 10:51:31.037265

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "21b0905294d5"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "clients",
        sa.Column("client_id", sa.Integer(), nullable=False),
        sa.Column("client_name", sa.String(length=20), nullable=False),
        sa.Column("client_patronymic", sa.String(length=20), nullable=False),
        sa.Column("client_surname", sa.String(length=20), nullable=False),
        sa.Column("passport_numb", sa.String(length=11), nullable=False),
        sa.Column("city", sa.String(length=20), nullable=False),
        sa.Column("phone_numb", sa.String(length=12), nullable=False),
        sa.PrimaryKeyConstraint("client_id", name=op.f("pk_clients")),
    )
    op.create_table(
        "deposits",
        sa.Column("deposit_id", sa.Integer(), nullable=False),
        sa.Column("deposit_name", sa.String(length=20), nullable=False),
        sa.Column("shelf_life", sa.Integer(), nullable=False),
        sa.Column("rate", sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint("deposit_id", name=op.f("pk_deposits")),
    )
    op.create_table(
        "users",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("user_name", sa.String(length=20), nullable=False),
        sa.Column("password_hash", sa.String(length=256), nullable=False),
        sa.Column(
            "role",
            sa.Enum(
                "admin",
                "deposit_manager",
                "bank_operator",
                "analyst",
                name="user_role",
            ),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("user_id", name=op.f("pk_users")),
        sa.UniqueConstraint("user_name", name=op.f("uq_users_user_name")),
    )
    op.create_table(
        "accounts",
        sa.Column("account_numb", sa.Integer(), nullable=False),
        sa.Column(
            "opening_date",
            sa.DateTime(),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.Column("closing_date", sa.DateTime(), nullable=True),
        sa.Column("amount_invested", sa.Integer(), nullable=False),
        sa.Column("deposit_id", sa.Integer(), nullable=False),
        sa.Column("client_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["client_id"],
            ["clients.client_id"],
            name=op.f("fk_accounts_accounts_client_id"),
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["deposit_id"],
            ["deposits.deposit_id"],
            name=op.f("fk_accounts_accounts_deposit_id"),
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("account_numb", name=op.f("pk_accounts")),
    )



def downgrade() -> None:
    """Downgrade schema."""

    op.drop_table("accounts")
    op.drop_table("users")
    op.drop_table("deposits")
    op.drop_table("clients")

