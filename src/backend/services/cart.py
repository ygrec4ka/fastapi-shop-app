import logging
from typing import Dict

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.schemas.cart import CartItemCreate, CartItemUpdate, CartItem, CartResponse
from backend.services.product import ProductService


class CartService:
    def __init__(
        self,
        session: AsyncSession,
        product_service: ProductService,
    ):
        self.session = session
        self.logger = logging.getLogger(__name__)
        self.product_service = product_service

    async def add_to_cart(
        self,
        cart_data: Dict[int, int],
        item: CartItemCreate,
    ) -> Dict[int, int]:
        product = await self.product_service.get_product_by_id(item.product_id)

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product {item.product_id} not found",
            )
        self.logger.info(
            "Added %s of product %s to cart",
            item.quantity,
            item.product_id,
        )

        cart_data.setdefault(item.product_id, 0)
        cart_data[item.product_id] += item.quantity

        return cart_data

    async def update_cart_item(
        self,
        cart_data: Dict[int, int],
        item: CartItemUpdate,
    ) -> Dict[int, int]:
        if item.product_id not in cart_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product_id: {item.product_id} not in cart",
            )
        cart_data[item.product_id] = item.quantity
        self.logger.info(
            "Updated product_id: %s quantity to %s", item.product_id, item.quantity
        )
        return cart_data

    async def remove_from_cart(
        self,
        cart_data: Dict[int, int],
        product_id: int,
    ) -> Dict[int, int]:
        if product_id in cart_data:
            quantity = cart_data.pop(product_id)
            self.logger.info(
                "Removed quantity: %s of product_id: %s from cart", quantity, product_id
            )
        return cart_data

    async def get_cart_details(
        self,
        cart_data: Dict[int, int],
    ) -> CartResponse:
        if not cart_data:
            return CartResponse(items=[], total=0.0, items_count=0)

        product_ids = list(cart_data.keys())
        products = await self.product_service.get_multiple_products_by_ids(product_ids)
        products_dict = {p.id: p for p in products}

        cart_items = []
        total_price = total_items = 0

        for product_id, quantity in cart_data.items():
            if product_id in products_dict:
                product = products_dict[product_id]
                subtotal = product.price * quantity
                cart_item = CartItem(
                    product_id=product.id,
                    name=product.name,
                    price=product.price,
                    quantity=quantity,
                    subtotal=subtotal,
                    image_url=product.image_url,
                )
                cart_items.append(cart_item)
                total_price += subtotal
                total_items += quantity

        return CartResponse(
            items=cart_items, total=round(total_price, 2), items_count=total_items
        )
