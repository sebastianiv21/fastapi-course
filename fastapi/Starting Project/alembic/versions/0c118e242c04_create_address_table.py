"""Create address table

Revision ID: 0c118e242c04
Revises: 021bb53e3157
Create Date: 2023-09-18 09:25:11.276872

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0c118e242c04"
down_revision: Union[str, None] = "021bb53e3157"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "address",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("address1", sa.String(), nullable=False),
        sa.Column("address2", sa.String(), nullable=False),
        sa.Column("city", sa.String(), nullable=False),
        sa.Column("state", sa.String(), nullable=False),
        sa.Column("country", sa.String(), nullable=False),
        sa.Column("postalcode", sa.String(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("address")
