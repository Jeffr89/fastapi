"""add user table

Revision ID: c3bdb5483794
Revises: 255d35d502d8
Create Date: 2022-01-09 23:31:32.175764

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c3bdb5483794"
down_revision = "255d35d502d8"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )


def downgrade():
    op.drop_table("users")
