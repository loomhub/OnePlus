"""Add change table name from llc_master to llcs

Revision ID: 663a899b6329
Revises: 738ed17555b6
Create Date: 2024-04-17 19:09:59.182592

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '663a899b6329'
down_revision: Union[str, None] = '738ed17555b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Rename the 'llc_master' table to 'llcs'
    op.rename_table('llc_master', 'llcs')


def downgrade() -> None:
    # Revert the table name from 'llcs' back to 'llc_master'
    op.rename_table('llcs', 'llc_master')
