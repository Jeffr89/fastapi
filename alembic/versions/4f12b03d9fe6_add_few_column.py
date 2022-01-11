"""add add few column

Revision ID: 4f12b03d9fe6
Revises: 759ce1f359b6
Create Date: 2022-01-10 17:49:00.865940

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "4f12b03d9fe6"
down_revision = "759ce1f359b6"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "posts",
        sa.Column("published", sa.Boolean, nullable=True, server_default="True"),
    )
    op.add_column(
        "posts",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
    )


def downgrade():
    op.drop_column("posts","published")
    op.drop_column("posts","created_at")
    pass
