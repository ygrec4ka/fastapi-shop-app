"""add category_id to products

Revision ID: f0feb277e822
Revises: 496648db1156
Create Date: 2026-02-27 19:06:17.629139

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "f0feb277e822"
down_revision: Union[str, Sequence[str], None] = "496648db1156"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("products", sa.Column("category_id", sa.Integer(), nullable=False))
    op.alter_column("products", "description", existing_type=sa.TEXT(), nullable=True)
    op.alter_column("products", "image_url", existing_type=sa.VARCHAR(), nullable=True)
    op.create_foreign_key(
        op.f("fk_products_category_id_categories"),
        "products",
        "categories",
        ["category_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint(
        op.f("fk_products_category_id_categories"),
        "products",
        type_="foreignkey",
    )
    op.alter_column("products", "image_url", existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column("products", "description", existing_type=sa.TEXT(), nullable=False)
    op.drop_column("products", "category_id")
