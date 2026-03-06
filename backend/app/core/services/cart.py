import logging
from typing import TYPE_CHECKING, Dict

from fastapi import HTTPException, status

from sqlalchemy import select, Result, Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.schemas.cart import CartItemCreate

if TYPE_CHECKING:
    from app.core.services.category import CategoryService
    from app.core.services.product import ProductService

class CartService:
    def __init__(
        self,
        session: AsyncSession,
        category_service: "CategoryService",
        product_service: "ProductService",
    ):
        self.session = session
        self.logger = logging.getLogger(__name__)
        self.category_service = category_service
        self.product_service = product_service


    async def add_to_cart(self, cart_data:Dict[int, int], item: CartItemCreate) -> Dict[int, int]:
        product = self.product_service.get_product_by_id(item.product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {item.product_id} not found",
            )

        if item.product_id in cart_data:
            cart_data[item.product_id] += item.quantity
        else:
            cart_data[item.product_id] = item.quantity