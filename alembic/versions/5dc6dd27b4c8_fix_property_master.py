"""Fix property_master

Revision ID: 5dc6dd27b4c8
Revises: a5c5f3a00b42
Create Date: 2024-04-17 18:48:45.786483

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5dc6dd27b4c8'
down_revision: Union[str, None] = 'a5c5f3a00b42'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Remove property_name from the primary key
    op.drop_constraint('property_master_pkey', 'property_master', type_='primary')
    op.create_primary_key(None, 'property_master', ['id'])

    # Add a unique constraint to llc
    op.create_unique_constraint('uix_property_name', 'property_master', ['property_name'])


def downgrade() -> None:
    # Revert to previous state where property_name was part of the primary key
    op.drop_constraint('uix_property_name', 'property_master', type_='unique')
    op.create_primary_key(None, 'property_master', ['id', 'property_name'])

