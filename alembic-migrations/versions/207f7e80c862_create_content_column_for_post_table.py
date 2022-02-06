"""create content column for post table

Revision ID: 207f7e80c862
Revises: 1307638814eb
Create Date: 2022-02-06 11:57:44.147645

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '207f7e80c862'
down_revision = '1307638814eb'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'posts',
        sa.Column('content', sa.String, nullable=False)
    )
    pass


def downgrade():
    op.drop_column(
        'posts',
        'content'
    )
    pass
