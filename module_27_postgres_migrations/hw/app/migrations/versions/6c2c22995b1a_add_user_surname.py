"""add user.surname

Revision ID: 6c2c22995b1a
Revises: 9333fda2cdd6
Create Date: 2025-01-21 16:12:56.394823

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6c2c22995b1a'
down_revision: Union[str, None] = '9333fda2cdd6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('user', sa.Column('surname', sa.String(length=50), nullable=True))


def downgrade() -> None:
    op.drop_column('user', 'surname')
