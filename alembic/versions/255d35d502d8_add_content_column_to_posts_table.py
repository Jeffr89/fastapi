"""add content column to posts table

Revision ID: 255d35d502d8
Revises: 1f8e73dc78c1
Create Date: 2022-01-09 23:27:03.994258

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '255d35d502d8'
down_revision = '1f8e73dc78c1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))


def downgrade():
    op.drop_column("posts", "content")
