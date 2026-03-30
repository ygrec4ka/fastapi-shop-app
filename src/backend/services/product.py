import logging
from typing import Sequence, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
from sqlalchemy.orm import joinedload

from backend.core.exceptions import EntityNotFoundError
from backend.core.schemas.product import ProductCreate
from backend.core.models import Product, Category

log = logging.getLogger(__name__)


class ProductService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_new_product(self, product_data: ProductCreate) -> Product:
        new_product = Product(**product_data.model_dump())
        self.session.add(new_product)
        await self.session.commit()
        await self.session.refresh(new_product)
        log.info("Product created: %s", new_product.id)
        return new_product

    async def get_product_by_id(self, product_id: int) -> Product:
        stmt = (
            select(Product)
            .where(Product.id == product_id)
            .options(joinedload(Product.category))
        )

        result: Result = await self.session.execute(stmt)
        product = result.unique().scalar_one_or_none()

        if not product:
            raise EntityNotFoundError(f"Product not found with id: {product_id}")

        return product

    async def get_multiple_products_by_ids(
        self, product_ids: List[int]
    ) -> Sequence[Product]:
        if not product_ids:
            return []

        stmt = (
            select(Product)
            .where(Product.id.in_(product_ids))
            .options(joinedload(Product.category))
        )
        result: Result = await self.session.execute(stmt)
        return result.unique().scalars().all()

    async def get_all_products(self) -> Sequence[Product]:
        stmt = (
            select(Product)
            .options(joinedload(Product.category))
            .order_by(Product.created_at.desc())
        )

        result: Result = await self.session.execute(stmt)
        return result.unique().scalars().all()

    async def get_products_by_category(self, category_id: int) -> Sequence[Product]:
        category = await self.session.get(Category, category_id)
        if not category:
            raise EntityNotFoundError(f"Category with id: {category_id} not found")

        stmt = (
            select(Product)
            .where(Product.category_id == category_id)
            .options(joinedload(Product.category))
            .order_by(Product.created_at.desc())
        )

        result: Result = await self.session.execute(stmt)
        return result.unique().scalars().all()
