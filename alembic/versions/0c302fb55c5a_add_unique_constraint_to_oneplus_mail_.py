"""Add unique constraint to oneplus_mail table

Revision ID: 0c302fb55c5a
Revises: b45c43f09ea5
Create Date: 2024-04-23 17:10:33.219521

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0c302fb55c5a'
down_revision: Union[str, None] = 'b45c43f09ea5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint('uix_mail', 'oneplus_mail', ['subject', 'receiver', 'cc', 'bcc'])


def downgrade() -> None:
    op.drop_constraint('uix_mail', 'oneplus_mail', type_='unique')
