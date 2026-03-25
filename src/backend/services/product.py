import logging
from typing import Sequence, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
from sqlalchemy.orm import joinedload, selectinload

from backend.core.exceptions import EntityNotFoundError
from backend.core.schemas.product import ProductCreate
from backend.core.models import Product, Category


class ProductService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.logger = logging.getLogger(__name__)

    async def create_new_product(self, product_data: ProductCreate) -> Product:
        self.logger.debug("Starting to create product")

        new_product = Product(**product_data.model_dump())
        self.logger.debug("Created new product object")

        self.session.add(new_product)
        await self.session.commit()
        await self.session.refresh(new_product)
        self.logger.info("Product created successfully: %s", new_product.id)

        return new_product

    async def get_product_by_id(self, product_id: int) -> Product:
        self.logger.debug("Starting to get product by id: %s", product_id)

        stmt = (
            select(Product)
            .where(Product.id == product_id)
            .options(
                joinedload(Product.category),
            )
        )

        result: Result = await self.session.execute(stmt)
        product = result.unique().scalar_one_or_none()

        if not product:
            self.logger.warning("Product not found: %s", product_id)
            raise EntityNotFoundError(f"Product not found with id: {product_id}")

        self.logger.debug("Product found: %s", product_id)
        return product

    async def get_multiple_products_by_ids(self, product_ids: List[int]) -> Sequence[Product]:
        self.logger.debug("Fetching multiple products: %s", product_ids)
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
        self.logger.debug("Starting to get all products")

        stmt = (select(Product).options(joinedload(Product.category))).order_by(
            Product.created_at.desc()
        )

        result: Result = await self.session.execute(stmt)
        all_products = result.unique().scalars().all()
        self.logger.info("Retrieved %d products", len(all_products))

        return all_products

    async def get_products_by_category(self, category_id: int) -> Sequence[Product]:
        self.logger.debug("Starting to get products by category: %s", category_id)

        category = await self.session.get(Category, category_id)
        if not category:
            self.logger.warning("Category not found: %s", category_id)
            raise EntityNotFoundError(f"Category with id: {category_id} not found")
        self.logger.debug("Category found: %s", category_id)

        stmt = (
            select(Product)
            .where(Product.category_id == category_id)
            .options(
                joinedload(Product.category),
                selectinload(Product.image_url),
            )
            .order_by(Product.created_at.desc())
        )

        result: Result = await self.session.execute(stmt)
        products = result.unique().scalars().all()
        self.logger.info(
            "Retrieved %d products for category %s", len(products), category_id
        )

        return products

    async def get_multiple_products_by_ids(
        self, product_ids: List[int]
    ) -> Sequence[Product]:
        self.logger.debug("Starting to get multiple products by ids: %s", product_ids)

        stmt = (
            select(Product)
            .where(Product.id.in_(product_ids))
            .options(
                joinedload(Product.category),
                selectinload(Product.image_url),
            )
        )

        result: Result = await self.session.execute(stmt)
        products = result.unique().scalars().all()
        self.logger.info("Retrieved %d products by ids", len(products))

        return products
