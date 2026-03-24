from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Text, Float, DateTime, func, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from backend.core.models import Base

from backend.core.models.mixins.id_int_pk import IdIntPk

if TYPE_CHECKING:
    from backend.core.models import Category


class Product(Base, IdIntPk):

    name: Mapped[str] = mapped_column(nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    image_url: Mapped[str] = mapped_column(nullable=True)


    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    category_id: Mapped[int] = mapped_column(
        ForeignKey(
            "categories.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    category: Mapped["Category"] = relationship(
        back_populates="products",
    )

    def __repr__(self):
        return f"Product(id={self.id}, name={self.name}, price={self.price})"
