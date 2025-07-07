"""add few columns to posts

Revision ID: 4d54b940c1d9
Revises: ed0d12d98d54
Create Date: 2025-07-07 13:39:24.532118

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4d54b940c1d9'
down_revision: Union[str, Sequence[str], None] = 'ed0d12d98d54'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('published',sa.Boolean(),nullable=False,server_default='True'),)
    op.add_column('posts',sa.Column('created-at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
