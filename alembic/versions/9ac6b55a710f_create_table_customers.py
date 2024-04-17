"""Create table customers

Revision ID: 9ac6b55a710f
Revises: 5a4d597e7738
Create Date: 2024-04-17 19:50:34.108368

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9ac6b55a710f'
down_revision: Union[str, None] = '5a4d597e7738'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create the 'customers' table
    op.create_table(
        'customers',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('customer', sa.String, nullable=False, unique=True, index=True),
        sa.Column('recipient_type', sa.String, nullable=True),
        sa.Column('recipient_tin_type', sa.String, nullable=True),
        sa.Column('recipient_tin', sa.String),
        sa.Column('last_name', sa.String),
        sa.Column('first_name', sa.String),
        sa.Column('address', sa.String),
        sa.Column('city', sa.String),
        sa.Column('state', sa.String),
        sa.Column('zip_code', sa.String),
        sa.Column('country', sa.String),
        sa.UniqueConstraint('customer', name='uix_customer'),
        sa.CheckConstraint('recipient_type IN (\'Individual\',\'Business\')', name='ck_customer_recipient_type'),
        sa.CheckConstraint('recipient_tin_type IN (\'SSN\', \'EIN\')', name='ck_customer_tin_type')
    )



def downgrade() -> None:
    # Drop the 'vendors' table
    op.drop_table('customers')

