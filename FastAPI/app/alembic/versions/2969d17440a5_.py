"""empty message

Revision ID: 2969d17440a5
Revises: 1490b6e9778c
Create Date: 2024-10-26 16:20:49.005461

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2969d17440a5'
down_revision: Union[str, None] = '1490b6e9778c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass