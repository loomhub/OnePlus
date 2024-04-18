"""Create tennant master

Revision ID: 5c4725c41f49
Revises: f570025acf6c
Create Date: 2024-04-17 20:10:34.720649

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5c4725c41f49'
down_revision: Union[str, None] = 'f570025acf6c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create the 'tenants' table with appropriate columns and constraints
    op.create_table(
        'tenants',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('customer', sa.String, nullable=False, unique=True, index=True),
        sa.Column('property_name', sa.String, nullable=False, index=True),
        sa.Column('unit_name', sa.String),
        sa.Column('lease_start', sa.Date),
        sa.Column('lease_end', sa.Date),
        sa.Column('rent', sa.Numeric(10, 2)),
        sa.Column('security_deposit', sa.Numeric(10, 2)),
        sa.UniqueConstraint('customer', 'property_name', name='uix_tenant')
    )



def downgrade() -> None:
    # Drop the 'tenants' table
    op.drop_table('tenants')
