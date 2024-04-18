"""Create foreign keys on business rules logic

Revision ID: d85326c6a293
Revises: 298aa5012d6b
Create Date: 2024-04-17 22:15:02.265523

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd85326c6a293'
down_revision: Union[str, None] = '298aa5012d6b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Adding foreign key constraints after confirming the unique constraint exists
    op.create_foreign_key(
        'fk_business_rules_logic_transaction_group',
        'business_rules_logic', 'transaction_types',
        ['transaction_group','transaction_type'], ['transaction_group','transaction_type']
    )

def downgrade() -> None:
    # Drop the foreign key constraints
    op.drop_constraint('fk_business_rules_logic_transaction_group', 'business_rules_logic', type_='foreignkey')
