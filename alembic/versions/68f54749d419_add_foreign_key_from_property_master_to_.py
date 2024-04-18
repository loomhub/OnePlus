"""Add foreign key from property_master to llcs

Revision ID: 68f54749d419
Revises: 8e4e29b82316
Create Date: 2024-04-17 22:30:58.963860

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '68f54749d419'
down_revision: Union[str, None] = '8e4e29b82316'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
        # Adding foreign key constraints after confirming the unique constraint exists
    op.create_foreign_key(
        'fk_property_master_llc_llcs',
        'property_master', 'llcs',
        ['llc'], ['llc']
    )

def downgrade() -> None:
    # Removing the foreign key constraint from 'property_master'
    op.drop_constraint('fk_property_master_llc_llcs', 'property_master', type_='foreignkey')
    
