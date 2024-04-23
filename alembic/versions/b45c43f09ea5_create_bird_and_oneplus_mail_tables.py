"""Create bird and oneplus_mail tables

Revision ID: b45c43f09ea5
Revises: 3ef50c3ceb8a
Create Date: 2024-04-22 15:52:40.857996

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b45c43f09ea5'
down_revision: Union[str, None] = '3ef50c3ceb8a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('bird',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sender', sa.String(), nullable=False),
    sa.Column('pwd', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('sender', name='uix_sender'),
    sa.Index('ix_bird_sender', 'sender')
    )
    op.create_table('oneplus_mail',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('subject', sa.String(), nullable=False, index=True),
    sa.Column('receiver', sa.String(), nullable=False),
    sa.Column('cc', sa.String(), nullable=True),
    sa.Column('bcc', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('oneplus_mail')
    op.drop_table('bird')
