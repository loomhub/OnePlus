"""Add composite unique constraint to transactions

Revision ID: 738ed17555b6
Revises: 5dc6dd27b4c8
Create Date: 2024-04-17 19:05:15.941026

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '738ed17555b6'
down_revision: Union[str, None] = '5dc6dd27b4c8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add a composite unique constraint to the table 'transactions'
    op.create_unique_constraint(
        'uix_transaction',  # Constraint name
        'transactions',     # Table name
        ['date', 'description', 'details', 'amount']  # Columns included in the constraint
    )


def downgrade() -> None:
    op.drop_constraint(
        'uix_transaction',  # Constraint name
        'transactions',     # Table name
        type_='unique'      # Type of the constraint
    )
