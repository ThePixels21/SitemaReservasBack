"""autorevision migratios

Revision ID: 4d7ef29b00b8
Revises: 2969d17440a5
Create Date: 2024-10-26 16:20:50.045218

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4d7ef29b00b8"
down_revision: Union[str, None] = "2969d17440a5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('person', sa.Column('test', sa.String(length=250), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('person', 'test')
    # ### end Alembic commands ###
