"""Rename created-at to created_at

Revision ID: cc1a027df587
Revises: f242fc90a3d7
Create Date: 2025-07-09 13:20:52.690769

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cc1a027df587'
down_revision: Union[str, Sequence[str], None] = 'f242fc90a3d7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('posts', 'created-at', new_column_name='created_at')
    pass


def downgrade() -> None:
    op.alter_column('posts', 'created_at', new_column_name='created-at')
    pass
