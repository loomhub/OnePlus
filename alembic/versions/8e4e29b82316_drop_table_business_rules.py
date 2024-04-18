"""Drop table business_rules

Revision ID: 8e4e29b82316
Revises: d85326c6a293
Create Date: 2024-04-17 22:18:25.215160

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8e4e29b82316'
down_revision: Union[str, None] = 'd85326c6a293'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop the 'business_rules' table
    op.drop_table('business_rules')


def downgrade() -> None:
    # Create the 'business_rules' table with appropriate columns and constraints
    op.create_table(
        'business_rules',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('key1', sa.String, nullable=False, index=True),
        sa.Column('op1', sa.String, nullable=False, index=True),
        sa.Column('val1', sa.String, nullable=False, index=True),
        sa.Column('key2', sa.String, nullable=False, index=True),
        sa.Column('op2', sa.String, nullable=False, index=True),
        sa.Column('val2', sa.String, nullable=False, index=True),
        sa.Column('key3', sa.String, nullable=False, index=True),
        sa.Column('op3', sa.String, nullable=False, index=True),
        sa.Column('val3', sa.String, nullable=False, index=True),
        sa.Column('key4', sa.String, nullable=False, index=True),
        sa.Column('op4', sa.String, nullable=False, index=True),
        sa.Column('val4', sa.String, nullable=False, index=True),
        sa.Column('transaction_group', sa.String),
        sa.Column('transaction_type', sa.String),
        sa.Column('vendor', sa.String),
        sa.Column('customer', sa.String),
        sa.Column('vendor_w9', sa.String),
        sa.Column('customer_w9', sa.String),
        sa.UniqueConstraint('key1', 'op1', 'val1', 'key2', 'op2', 'val2', 'key3', 'op3', 'val3', 'key4', 'op4', 'val4', name='uix_business_rules_logic')
    )
