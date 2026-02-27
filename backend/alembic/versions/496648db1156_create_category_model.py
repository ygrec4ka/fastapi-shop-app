"""create category model

Revision ID: 496648db1156
Revises: 2ffe4155e11b
Create Date: 2026-02-27 18:31:07.304707

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "496648db1156"
down_revision: Union[str, Sequence[str], None] = "2ffe4155e11b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("slug", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_categories")),
    )
    op.create_index(op.f("ix_categories_id"), "categories", ["id"], unique=False)
    op.create_index(op.f("ix_categories_name"), "categories", ["name"], unique=True)
    op.create_index(op.f("ix_categories_slug"), "categories", ["slug"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_categories_slug"), table_name="categories")
    op.drop_index(op.f("ix_categories_name"), table_name="categories")
    op.drop_index(op.f("ix_categories_id"), table_name="categories")
    op.drop_table("categories")
