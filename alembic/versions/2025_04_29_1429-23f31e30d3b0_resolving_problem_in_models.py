"""resolving problem in models

Revision ID: 23f31e30d3b0
Revises: f345a35b0f1e
Create Date: 2025-04-29 14:29:20.122147

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "23f31e30d3b0"
down_revision: Union[str, None] = "f345a35b0f1e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "expenses", sa.Column("description", sa.String(length=255), nullable=True)
    )
    op.drop_column("expenses", "desciption")
    op.alter_column(
        "users",
        "username",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=255),
        existing_nullable=False,
    )
    op.drop_index("ix_users_username", table_name="users")
    op.create_unique_constraint(None, "users", ["username"])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "users", type_="unique")
    op.create_index("ix_users_username", "users", ["username"], unique=False)
    op.alter_column(
        "users",
        "username",
        existing_type=sa.String(length=255),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    op.add_column(
        "expenses",
        sa.Column(
            "desciption", sa.VARCHAR(length=255), autoincrement=False, nullable=True
        ),
    )
    op.drop_column("expenses", "description")
    # ### end Alembic commands ###
