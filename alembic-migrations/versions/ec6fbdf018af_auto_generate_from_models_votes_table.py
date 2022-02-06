"""Auto generate from models - Votes Table

Revision ID: ec6fbdf018af
Revises: d97f9991616e
Create Date: 2022-02-06 12:53:11.564109

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ec6fbdf018af'
down_revision = 'd97f9991616e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('votes',
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('post_id', 'user_id')
    )


def downgrade():
    op.drop_table('votes')