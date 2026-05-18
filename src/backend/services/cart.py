import logging
from typing import Optional

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.models import CartItem as CartItemModel, User
from backend.core.exceptions import EntityNotFoundError
from backend.core.schemas.cart import CartItemCreate, CartItemUpdate, CartResponse, CartItem
from backend.services.product import ProductService

log = logging.getLogger(__name__)


class CartService:
    def __init__(
        self,
        session: AsyncSession,
        product_service: ProductService,
    ):
        self.session = session
        self.product_service = product_service

    async def add_to_cart(
        self,
        item: CartItemCreate,
        user: User,
    ) -> None:
        await self.product_service.get_product_by_id(item.product_id)

        stmt = select(CartItemModel).where(
            CartItemModel.user_id == user.id,
            CartItemModel.product_id == item.product_id
        )
        result = await self.session.execute(stmt)
        cart_item = result.scalar_one_or_none()

        if cart_item:
            cart_item.quantity += item.quantity
        else:
            cart_item = CartItemModel(
                user_id=user.id,
                product_id=item.product_id,
                quantity=item.quantity
            )
            self.session.add(cart_item)

        await self.session.commit()

    async def update_cart_item(
        self,
        item: CartItemUpdate,
        user: User,
    ) -> None:
        stmt = select(CartItemModel).where(
            CartItemModel.user_id == user.id,
            CartItemModel.product_id == item.product_id
        )
        result = await self.session.execute(stmt)
        cart_item = result.scalar_one_or_none()

        if not cart_item:
            raise EntityNotFoundError("Item not found in user cart")

        if item.quantity <= 0:
            await self.session.delete(cart_item)
        else:
            cart_item.quantity = item.quantity

        await self.session.commit()

    async def remove_from_cart(
        self,
        product_id: int,
        user: User,
    ) -> None:
        stmt = delete(CartItemModel).where(
            CartItemModel.user_id == user.id,
            CartItemModel.product_id == product_id
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_cart_details(
        self,
        user: User,
    ) -> CartResponse:
        stmt = select(CartItemModel).where(CartItemModel.user_id == user.id)
        result = await self.session.execute(stmt)
        user_cart_items = result.scalars().all()

        if not user_cart_items:
            return CartResponse(items=[], total=0.0, items_count=0)

        product_ids = [item.product_id for item in user_cart_items]
        products = await self.product_service.get_multiple_products_by_ids(product_ids)
        products_dict = {p.id: p for p in products}

        cart_items = []
        total_price = total_items = 0

        for cart_item_model in user_cart_items:
            product = products_dict.get(cart_item_model.product_id)
            if product:
                subtotal = product.price * cart_item_model.quantity
                cart_item = CartItem(
                    product_id=product.id,
                    name=product.name,
                    price=product.price,
                    quantity=cart_item_model.quantity,
                    subtotal=subtotal,
                    image_url=product.image_url,
                )
                cart_items.append(cart_item)
                total_price += subtotal
                total_items += cart_item_model.quantity

        return CartResponse(
            items=cart_items,
            total=round(total_price, 2),
            items_count=total_items,
        )
