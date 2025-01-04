"""Add indexes to TransportType

Revision ID: 8840e437f81f
Revises: 548c75949b97
Create Date: 2025-01-04 21:47:09.269177

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8840e437f81f'
down_revision: Union[str, None] = '548c75949b97'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
   op.create_index('ix_routes_description', 'routes', ['description'])  # Index on description column
op.create_index('ix_routes_priority', 'routes', ['priority'])

def downgrade() -> None:
    # Удаление индексов при откате миграции
    op.drop_index('ix_routes_description', table_name='routes')
    op.drop_index('ix_routes_priority', table_name='routes')
