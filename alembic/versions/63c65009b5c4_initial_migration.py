"""Initial migration

Revision ID: 63c65009b5c4
Revises: 
Create Date: 2025-01-03 12:55:44.266084

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '63c65009b5c4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transport_types', sa.Column('year_of_release', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('transport_types', 'year_of_release')
    # ### end Alembic commands ###
