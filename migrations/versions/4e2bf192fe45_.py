"""empty message

Revision ID: 4e2bf192fe45
Revises: 16fbe33cb234
Create Date: 2024-07-15 20:32:01.768332

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4e2bf192fe45'
down_revision: Union[str, None] = '16fbe33cb234'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bookings', sa.Column('selected_times', sa.JSON(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('bookings', 'selected_times')
    # ### end Alembic commands ###
