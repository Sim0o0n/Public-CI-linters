"""add user.patronomic

Revision ID: d3dcb6ebb7f4
Revises: 6c2c22995b1a
Create Date: 2025-01-21 16:22:55.206184

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd3dcb6ebb7f4'
down_revision: Union[str, None] = '6c2c22995b1a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('user', sa.Column('patronomic', sa.String(length=50), nullable=True))


def downgrade() -> None:
    op.drop_column('user', 'patronomic')
