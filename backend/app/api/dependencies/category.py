from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import db_helper
from app.core.services.category import CategoryService


def get_category_services(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return CategoryService(session)
