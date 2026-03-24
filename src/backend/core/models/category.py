from typing import TYPE_CHECKING, List

from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship
from backend.core.models import Base

from backend.core.models.mixins.id_int_pk import IdIntPk

if TYPE_CHECKING:
    from backend.core.models import Product


class Category(Base, IdIntPk):
    __tablename__ = "categories"
    
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
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name})>"
