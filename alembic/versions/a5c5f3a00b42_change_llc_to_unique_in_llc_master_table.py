"""Change llc to unique in llc_master table

Revision ID: a5c5f3a00b42
Revises: a3785600ad21
Create Date: 2024-04-17 18:43:01.990130

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a5c5f3a00b42'
down_revision: Union[str, None] = 'a3785600ad21'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Remove llc from the primary key
    op.drop_constraint('llc_master_pkey', 'llc_master', type_='primary')
    op.create_primary_key(None, 'llc_master', ['id'])

    # Add a unique constraint to llc
    op.create_unique_constraint('uix_llc', 'llc_master', ['llc'])


def downgrade() -> None:
    # Revert to previous state where llc was part of the primary key
    op.drop_constraint('uix_llc', 'llc_master', type_='unique')
    op.create_primary_key(None, 'llc_master', ['id', 'llc'])
