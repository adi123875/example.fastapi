"""hash existing plain text passwords

Revision ID: 06d3d3afa9b3
Revises: cc1a027df587
Create Date: 2025-09-16 23:40:28.480427

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app import utils
Base = sa.orm.declarative_base()
# revision identifiers, used by Alembic.
revision: str = '06d3d3afa9b3'
down_revision: Union[str, Sequence[str], None] = 'cc1a027df587'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

class User(Base):
    __tablename__ = "users"   # change if your table is different
    id = sa.Column(sa.Integer, primary_key=True)
    password = sa.Column(sa.String)

def upgrade() -> None:
    bind = op.get_bind()
    session = Session(bind=bind)

    users = session.query(User).all()
    for user in users:
        if user.password and not user.password.startswith("$2b$"):  
            # bcrypt hashes start with $2b$, so only hash plain text
            user.password = utils.hash(user.password)
    session.commit()                       

def downgrade() -> None:
    """Downgrade schema."""
    pass
