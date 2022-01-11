"""add foreign-key to posts table

Revision ID: 759ce1f359b6
Revises: c3bdb5483794
Create Date: 2022-01-09 23:43:47.623717

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "759ce1f359b6"
down_revision = "c3bdb5483794"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("owner_id", sa.Integer, nullable=False))
    op.create_foreign_key(
        "post_user_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE"
    )


def downgrade():
    op.drop_constraint('post_user_fk', table_name="posts")
    op.drop_column("posts", "owner_id")
