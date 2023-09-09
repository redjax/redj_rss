"""Initial commit.

Revision ID: 40608f77da7c
Revises: a6585ebaf71d
Create Date: 2023-09-09 00:50:25.962207

"""
from __future__ import annotations

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "40608f77da7c"
down_revision: Union[str, None] = "a6585ebaf71d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
