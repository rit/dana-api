"""add collections table

Revision ID: e345d431f346
Revises:
Create Date: 2017-05-24 16:46:22.935909

"""
from alembic import op
import sqlalchemy as sa
# from sqlalchemy.dialects import postgresql import *

# revision identifiers, used by Alembic.
revision = 'e345d431f346'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('collections',
                    sa.Column('slug', sa.VARCHAR, primary_key=True),
                    sa.Column('parent_slug', sa.String, index=True),
                    sa.Column('label', sa.VARCHAR, nullable=False),
                    sa.Column('doc', sa.JSON, nullable=False))


def downgrade():
    op.drop_table('collections')
