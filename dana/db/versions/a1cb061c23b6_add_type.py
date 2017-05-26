"""Add type

Revision ID: a1cb061c23b6
Revises: e345d431f346
Create Date: 2017-05-26 00:16:10.614237

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1cb061c23b6'
down_revision = 'e345d431f346'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('collections', sa.Column('type', sa.VARCHAR))


def downgrade():
    op.drop_column('collections', 'type')
