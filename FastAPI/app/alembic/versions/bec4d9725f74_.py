"""empty message

Revision ID: bec4d9725f74
Revises: 4d7ef29b00b8
Create Date: 2024-10-26 16:40:58.756522

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "bec4d9725f74"
down_revision: Union[str, None] = "4d7ef29b00b8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
