"""Track collection ordering

Revision ID: 15baf2135742
Revises: 8400cb413b5e
Create Date: 2017-05-29 15:42:03.207594

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '15baf2135742'
down_revision = '8400cb413b5e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('collections', sa.Column('position', sa.INTEGER, server_default='-1'))


def downgrade():
    op.drop_column('collections', 'position')
