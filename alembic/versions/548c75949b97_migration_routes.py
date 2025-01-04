"""migration routes

Revision ID: 548c75949b97
Revises: 
Create Date: 2025-01-04 21:34:00.565557

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '548c75949b97'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Adding new columns 'description' and 'priority' to the 'routes' table
    op.add_column('routes', sa.Column('description', sa.Text(), nullable=True))  # Optional column
    op.add_column('routes', sa.Column('priority', sa.Integer(), nullable=True))  # Optional column

def downgrade() -> None:
    # Dropping the added columns 'description' and 'priority'
    op.drop_column('routes', 'description')
    op.drop_column('routes', 'priority')
