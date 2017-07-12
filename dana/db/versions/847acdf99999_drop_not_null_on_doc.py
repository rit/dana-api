"""drop not null on doc

Revision ID: 847acdf99999
Revises: a1cb061c23b6
Create Date: 2017-05-27 09:22:35.699560

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '847acdf99999'
down_revision = 'a1cb061c23b6'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('collections', 'doc', nullable=True)


def downgrade():
    op.alter_column('collections', 'doc', nullable=False)
