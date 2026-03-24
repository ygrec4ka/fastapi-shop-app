from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.models import db_helper
from backend.services.product import ProductService


def get_product_service(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return ProductService(session)
