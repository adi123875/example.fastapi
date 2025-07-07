"""add content column

Revision ID: 4a20276eeb72
Revises: ff4321d917cb
Create Date: 2025-06-27 23:37:41.059974

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4a20276eeb72'
down_revision: Union[str, Sequence[str], None] = 'ff4321d917cb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() :
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
