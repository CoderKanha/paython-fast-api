"""add foreign-key of owner_id to posts table

Revision ID: d97f9991616e
Revises: d716d938c681
Create Date: 2022-02-06 12:31:33.034485

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd97f9991616e'
down_revision = 'd716d938c681'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'posts',
        sa.Column('owner_id', sa.Integer(), nullable=False)
    )
    op.create_foreign_key('posts_owner_id_fkey', source_table='posts', referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint('posts_owner_id_fkey', 'posts')
    op.drop_column('posts', 'owner_id')
    pass
