"""Fix Trnsactions table

Revision ID: f570025acf6c
Revises: 9ac6b55a710f
Create Date: 2024-04-17 20:01:40.566766

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f570025acf6c'
down_revision: Union[str, None] = '9ac6b55a710f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop the existing 'transactions' table if it exists
    op.drop_table('transactions', if_exists=True)
    
    # Create the new 'transactions' table with the specified schema and foreign key
    op.create_table(
        'transactions',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('date', sa.Date, nullable=False, index=True),
        sa.Column('description', sa.String, nullable=False, index=True),
        sa.Column('details', sa.String, nullable=False, index=True),
        sa.Column('amount', sa.Numeric(10, 2), nullable=False, index=True),
        sa.Column('classification', sa.String),
        sa.Column('property_name', sa.String, sa.ForeignKey('property_master.property_name'), nullable=True),
        sa.Column('transaction_group', sa.String),
        sa.Column('transaction_type', sa.String),
        sa.Column('vendor', sa.String),
        sa.Column('customer', sa.String),
        sa.Column('comments', sa.String),
        sa.UniqueConstraint('date', 'description', 'details', 'amount', name='uix_transaction')
    )


def downgrade() -> None:
    # Drop the newly created 'transactions' table
    op.drop_table('transactions')
