"""Restart alembic after lost stage

Revision ID: 34013e38ecac
Revises: 5c4725c41f49
Create Date: 2024-04-17 21:51:57.676688

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'edd1cd227046'
down_revision: Union[str, None] = '34013e38ecac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
