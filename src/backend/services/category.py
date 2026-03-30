import logging

from sqlalchemy import select, Result, Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.exceptions import EntityNotFoundError
from backend.core.schemas.category import CategoryCreate
from backend.core.models import Category

log = logging.getLogger(__name__)


class CategoryService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_new_category(self, category_data: CategoryCreate) -> Category:
        new_category = Category(**category_data.model_dump())
        self.session.add(new_category)
        await self.session.commit()
        await self.session.refresh(new_category)
        log.info("Category created: %s", new_category.id)
        return new_category

    async def get_category_by_id(self, category_id: int) -> Category:
        category = await self.session.get(Category, category_id)
        if not category:
            raise EntityNotFoundError(f"Category not found with id: {category_id}")
        return category

    async def get_all_categories(self) -> Sequence[Category]:
        stmt = select(Category)
        result: Result = await self.session.execute(stmt)
        return result.scalars().all()

    async def delete_category(self, category_id: int) -> None:
        category = await self.session.get(Category, category_id)
        if not category:
            raise EntityNotFoundError(f"Category not found with id: {category_id}")

        await self.session.delete(category)
        await self.session.commit()
        log.info("Category deleted: %s", category_id)
