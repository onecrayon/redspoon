"""Init Users

Revision ID: d34d2a738ae3
Revises: 4a922b8683b6
Create Date: 2019-11-23 22:06:09.452829+00:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

import application.utils.alembic_helpers as utils

# revision identifiers, used by Alembic.
revision = 'd34d2a738ae3'
down_revision = '4a922b8683b6'
branch_labels = None
depends_on = None


def upgrade():
    utils.ensure_uuids_available()

    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=256), nullable=True),
        sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(['uuid'], ['global_uuids.uuid'], ondelete='cascade'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('uuid')
    )

    utils.create_trigger_for_table('users')


def downgrade():
    utils.drop_trigger_for_table('users')
    op.drop_table('users')
