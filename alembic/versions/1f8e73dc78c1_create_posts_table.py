"""create posts table

Revision ID: 1f8e73dc78c1
Revises: 
Create Date: 2022-01-09 14:20:03.953692

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1f8e73dc78c1"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
    )
    pass


def downgrade():
    op.drop_table("posts")
