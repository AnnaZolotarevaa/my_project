"""index status

Revision ID: 35257b6fe5cc
Revises: 3da8e1506527
Create Date: 2025-01-03 19:13:33.380217

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '35257b6fe5cc'
down_revision: Union[str, None] = '3da8e1506527'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Заполнение значений NULL значением по умолчанию 'active' перед изменением на NOT NULL
    op.execute("UPDATE routes SET status = 'active' WHERE status IS NULL")
    
    # Теперь можно безопасно изменить колонку на NOT NULL
    op.alter_column('routes', 'status',
                    existing_type=sa.VARCHAR(length=50),
                    nullable=False)
    
    # Создание индекса на колонку status
    op.create_index('ix_routes_status', 'routes', ['status'], unique=False)


def downgrade() -> None:
    # Удаление индекса на колонку status
    op.drop_index('ix_routes_status', table_name='routes')
    
    # При откате миграции возвращаем колонку 'status' в nullable=True
    op.alter_column('routes', 'status',
                    existing_type=sa.VARCHAR(length=50),
                    nullable=True)

    # ### end Alembic commands ###
