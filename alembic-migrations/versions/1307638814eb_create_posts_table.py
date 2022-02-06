"""create posts table

Revision ID: 1307638814eb
Revises: 
Create Date: 2022-02-06 11:51:19.945556

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1307638814eb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('title', sa.String, nullable=False)
    )
    pass


def downgrade():
    op.drop_table('posts')
    pass
