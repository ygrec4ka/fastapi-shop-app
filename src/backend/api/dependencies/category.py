from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.models import db_helper
from backend.services.category import CategoryService


def get_category_service(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return CategoryService(session)
