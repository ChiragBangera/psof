"""name-sdesc nullable false

Revision ID: c396ba9e3cd0
Revises: 075f27cc5cdd
Create Date: 2025-04-07 22:27:25.768154

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c396ba9e3cd0"
down_revision: Union[str, None] = "075f27cc5cdd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("user", "username", nullable=False)
    op.alter_column("user", "short_description", nullable=False)


def downgrade() -> None:
    op.alter_column("user", "username", nullable=True)
    op.alter_column("user", "short_description", nullable=True)
