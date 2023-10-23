"""add column to posts table

Revision ID: 66de2ebd37ca
Revises: 5671925bc3d0
Create Date: 2023-10-23 16:35:00.495716

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '66de2ebd37ca'
down_revision: Union[str, None] = '5671925bc3d0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_columns('posts',sa.Column('content', sa.String(), nullable=False))


def downgsrade() -> None:
    op.drop_column('posts')
