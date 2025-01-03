"""capacity migration and index

Revision ID: 74c378962836
Revises: 35257b6fe5cc
Create Date: 2025-01-03 19:36:41.650787

"""
from alembic import op
import sqlalchemy as sa
from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = '74c378962836'
down_revision: Union[str, None] = '35257b6fe5cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Добавление новой колонки 'capacity' в таблицу 'transport_types'
    op.add_column('transport_types', sa.Column('capacity', sa.Integer(), nullable=True))

    # Добавление индекса на колонку 'capacity'
    op.create_index('ix_transport_types_capacity', 'transport_types', ['capacity'], unique=False)

    # Добавление CHECK constraint, чтобы значение capacity не было равно 0
    op.execute('ALTER TABLE transport_types ADD CONSTRAINT chk_capacity_non_zero CHECK (capacity != 0)')


def downgrade() -> None:
    # Удаление CHECK constraint
    op.execute('ALTER TABLE transport_types DROP CONSTRAINT chk_capacity_non_zero')

    # Удаление индекса на колонку 'capacity'
    op.drop_index('ix_transport_types_capacity', table_name='transport_types')

    # Удаление колонки 'capacity' из таблицы 'transport_types'
    op.drop_column('transport_types', 'capacity')
