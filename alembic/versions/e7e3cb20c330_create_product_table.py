"""create_product_table

Revision ID: e7e3cb20c330
Revises: 
Create Date: 2026-09-27 11:50:34.422347

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e7e3cb20c330'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    tables = inspector.get_table_names()

    if 'product' not in tables:
        op.create_table(
            'product',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('name', sa.String(), nullable=False),
            sa.Column('description', sa.String(), nullable=True),
            sa.Column('price', sa.Float(), nullable=False),
            sa.Column('quantity', sa.Integer(), nullable=False),
            sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_product_id'), 'product', ['id'], unique=False)
        op.create_index(op.f('ix_product_name'), 'product', ['name'], unique=False)
    else:
        op.alter_column('product', 'name',
                   existing_type=sa.VARCHAR(),
                   nullable=False)
        op.alter_column('product', 'price',
                   existing_type=sa.DOUBLE_PRECISION(precision=53),
                   nullable=False)
        op.alter_column('product', 'quantity',
                   existing_type=sa.INTEGER(),
                   nullable=False)
        
        indexes = [idx['name'] for idx in inspector.get_indexes('product')]
        if 'ix_product_name' not in indexes:
            op.create_index(op.f('ix_product_name'), 'product', ['name'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_product_name'), table_name='product')
    op.drop_index(op.f('ix_product_id'), table_name='product')
    op.drop_table('product')
