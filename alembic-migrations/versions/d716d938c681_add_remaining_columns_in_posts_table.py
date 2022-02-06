"""add remaining columns in posts table

Revision ID: d716d938c681
Revises: 26dbf5d5cec2
Create Date: 2022-02-06 12:19:48.906872

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd716d938c681'
down_revision = '26dbf5d5cec2'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('is_published', sa.Boolean(), nullable=False, server_default=sa.text('True')))
    op.add_column('posts', sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default=sa.text('False')))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')))
    op.add_column('posts', sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')))
    pass


def downgrade():
    op.drop_column('posts', 'is_published')
    op.drop_column('posts', 'is_deleted')
    op.drop_column('posts', 'created_at')
    op.drop_column('posts', 'updated_at')
    pass
