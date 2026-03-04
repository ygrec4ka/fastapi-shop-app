import logging

from fastapi import HTTPException, status

from sqlalchemy import select, Result, Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.models import Category
from backend.core.schemas.category import CategoryCreate


class CategoryService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.logger = logging.getLogger(__name__)


    async def create_new_category(self, category_data: CategoryCreate) -> Category:
        self.logger.debug("Starting to create category")

        new_category = Category(**category_data.model_dump())
        self.logger.debug("Created new category object")

        self.session.add(new_category)
        await self.session.commit()
        await self.session.refresh(new_category)
        self.logger.info("Category created successfully: %s", new_category.id)

        return new_category


    async def get_category_by_id(self, category_id: int) -> Category:
        self.logger.debug("Starting to get category by id: %s", category_id)

        category = self.session.get(Category, category_id)
        if not category:
            self.logger.warning("Category not found: %s", category_id)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )

        self.logger.debug("Category found: %s", category.id)
        return category


    async def get_all_categories(self) -> Sequence[Category]:
        self.logger.debug("Starting to get all categories")

        stmt = select(Category)
        result: Result = await self.session.execute(stmt)

        all_categories = result.scalars().all()
        self.logger.info("Retrieved %d categories", len(all_categories))

        return all_categories


    async def delete_category(self, category_id: int) -> None:
        self.logger.debug("Starting to delete category: %s", category_id)

        category = self.session.get(Category, category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )

        await self.session.delete(category)
        await self.session.commit()
        self.logger.info("Category deleted successfully: %s", category_id)