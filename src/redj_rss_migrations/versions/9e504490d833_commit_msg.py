"""${commit_msg}.

Revision ID: 9e504490d833
Revises: 17c328a624be
Create Date: 2023-09-09 02:34:56.318951

"""
from __future__ import annotations

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "9e504490d833"
down_revision: Union[str, None] = "17c328a624be"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
