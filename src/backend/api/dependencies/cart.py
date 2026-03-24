from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.dependencies import get_product_service

from backend.core.models import db_helper

from backend.services.cart import CartService
from backend.services.product import ProductService


def get_cart_service(
    session: AsyncSession = Depends(db_helper.session_getter),
    product_service: ProductService = Depends(get_product_service),
):
    return CartService(
        session=session,
        product_service=product_service,
    )
