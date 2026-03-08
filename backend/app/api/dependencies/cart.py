from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.category import get_category_service
from app.api.dependencies.product import get_product_service

from app.core.models import db_helper

from app.core.services.cart import CartService
from app.core.services.category import CategoryService
from app.core.services.product import ProductService


def get_cart_service(
    session: AsyncSession = Depends(db_helper.session_getter),
    product_service: ProductService = Depends(get_product_service),
    category_service: CategoryService = Depends(get_category_service),
):
    return CartService(
        session=session,
        product_service=product_service,
        category_service=category_service,
    )
