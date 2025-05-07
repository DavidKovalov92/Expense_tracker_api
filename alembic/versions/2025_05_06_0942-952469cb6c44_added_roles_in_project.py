from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "952469cb6c44"
down_revision = "3063ac2c8451"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade schema."""
    user_role_enum = postgresql.ENUM("USER", "ADMIN", name="userrole")
    user_role_enum.create(op.get_bind())

    op.add_column(
        "users",
        sa.Column("role", user_role_enum, nullable=False, server_default="USER"),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column("users", "role")

    user_role_enum = postgresql.ENUM("USER", "ADMIN", name="userrole")
    user_role_enum.drop(op.get_bind())
