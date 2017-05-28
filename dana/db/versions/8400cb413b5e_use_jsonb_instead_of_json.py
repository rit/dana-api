"""Use jsonb instead of json

Revision ID: 8400cb413b5e
Revises: 847acdf99999
Create Date: 2017-05-27 11:41:08.043756

"""
from alembic import op
# import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as sa


# revision identifiers, used by Alembic.
revision = '8400cb413b5e'
down_revision = '847acdf99999'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('collections', 'doc', type_=sa.JSONB, postgresql_using='doc::jsonb')


def downgrade():
    op.alter_column('collections', 'doc', type_=sa.JSON, postgresql_using='doc::json')
