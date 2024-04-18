"""Create tenant master foreign keys

Revision ID: 38fe36c5f950
Revises: cb747f40bb46
Create Date: 2024-04-17 22:50:23.833401

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '38fe36c5f950'
down_revision: Union[str, None] = 'cb747f40bb46'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
     # Adding foreign key constraints after confirming the unique constraint exists
    op.create_foreign_key(
        'fk_tenants_customers_customer',
        'tenants', 'customers',
        ['customer'], ['customer']
    )
    op.create_foreign_key(
        'fk_tenants_property_master_property_name',
        'tenants', 'property_master',
        ['property_name'], ['property_name']
    )


def downgrade() -> None:
    # Removing the foreign key constraint from 'tenants'
    op.drop_constraint('fk_tenants_customers_customer', 'tenants', type_='foreignkey')
    op.drop_constraint('fk_tenants_property_master_property_name', 'tenants', type_='foreignkey')
