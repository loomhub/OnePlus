"""Create table vendors

Revision ID: 5a4d597e7738
Revises: 663a899b6329
Create Date: 2024-04-17 19:43:00.978344

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5a4d597e7738'
down_revision: Union[str, None] = '663a899b6329'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create the 'vendors' table
    op.create_table(
        'vendors',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('vendor', sa.String, nullable=False, unique=True, index=True),
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
        sa.UniqueConstraint('vendor', name='uix_vendor'),
        sa.CheckConstraint('recipient_type IN (\'Individual\',\'Business\')', name='ck_vendor_recipient_type'),
        sa.CheckConstraint('recipient_tin_type IN (\'SSN\', \'EIN\')', name='ck_vendor_tin_type')
    )



def downgrade() -> None:
    # Drop the 'vendors' table
    op.drop_table('vendors')
