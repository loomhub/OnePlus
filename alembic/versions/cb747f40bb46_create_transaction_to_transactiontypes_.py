"""Create Transaction to TransactionTypes Foreign Keys

Revision ID: cb747f40bb46
Revises: 68f54749d419
Create Date: 2024-04-17 22:38:36.343959

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cb747f40bb46'
down_revision: Union[str, None] = '68f54749d419'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Adding foreign key constraints after confirming the unique constraint exists
    op.create_foreign_key(
        'fk_transactions_transaction_types',
        'transactions', 'transaction_types',
        ['transaction_group','transaction_type'], ['transaction_group','transaction_type']
    )


def downgrade() -> None:
     # Drop the foreign key constraints
    op.drop_constraint('fk_transactions_transaction_types', 'transactions', type_='foreignkey')
    

