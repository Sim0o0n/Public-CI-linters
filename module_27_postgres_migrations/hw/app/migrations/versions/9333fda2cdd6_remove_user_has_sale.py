"""remove user.has_sale

Revision ID: 9333fda2cdd6
Revises: 
Create Date: 2025-01-21 16:05:58.195157

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9333fda2cdd6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('user', 'has_sale')


def downgrade() -> None:
    op.add_column('user', sa.Column('has_sale', sa.Boolean(), nullable=True))
