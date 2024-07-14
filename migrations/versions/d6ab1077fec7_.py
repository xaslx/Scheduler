"""empty message

Revision ID: d6ab1077fec7
Revises: 8725f4e5a9a9
Create Date: 2024-07-10 18:48:05.806133

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd6ab1077fec7'
down_revision: Union[str, None] = '8725f4e5a9a9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('date_for_booking', sa.JSON(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'date_for_booking')
    # ### end Alembic commands ###
