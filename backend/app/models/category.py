from typing import TYPE_CHECKING, List

from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship
from backend.app.models import Base

if TYPE_CHECKING:
    from backend.app.models import Product


class Category(Base):

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )
    name: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )
    slug: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )

    products: Mapped[List["Product"]] = relationship(
        back_populates="category",
    )

    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name})>"
