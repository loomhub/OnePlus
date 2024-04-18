"""Try creating foreign key again

Revision ID: 298aa5012d6b
Revises: 21955601e94b
Create Date: 2024-04-17 22:10:36.183164

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '298aa5012d6b'
down_revision: Union[str, None] = '21955601e94b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Adding foreign key constraints after confirming the unique constraint exists
    op.create_foreign_key(
        'fk_business_rules_transaction_group',
        'business_rules', 'transaction_types',
        ['transaction_group','transaction_type'], ['transaction_group','transaction_type']
    )


def downgrade() -> None:
    # Drop the foreign key constraints
    op.drop_constraint('fk_business_rules_transaction_group', 'business_rules', type_='foreignkey')
    
