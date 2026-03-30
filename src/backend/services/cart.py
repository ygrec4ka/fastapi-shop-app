import logging
from typing import Dict, Optional
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.models import CartItem as CartItemModel, User
from backend.core.exceptions import EntityNotFoundError
from backend.core.schemas.cart import CartItemCreate, CartItemUpdate, CartItem, CartResponse
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

    async def get_user_cart_dict(self, user: User) -> Dict[int, int]:
        stmt = select(CartItemModel).where(CartItemModel.user_id == user.id)
        result = await self.session.execute(stmt)
        items = result.scalars().all()
        return {item.product_id: item.quantity for item in items}

    async def add_to_cart(
        self,
        cart_data: Dict[int, int],
        item: CartItemCreate,
        user: Optional[User] = None,
    ) -> Dict[int, int]:
        await self.product_service.get_product_by_id(item.product_id)

        if user:
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
            return await self.get_user_cart_dict(user)

        cart_data.setdefault(item.product_id, 0)
        cart_data[item.product_id] += item.quantity
        return cart_data

    async def update_cart_item(
        self,
        cart_data: Dict[int, int],
        item: CartItemUpdate,
        user: Optional[User] = None,
    ) -> Dict[int, int]:
        if user:
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
            return await self.get_user_cart_dict(user)

        if item.product_id not in cart_data:
            raise EntityNotFoundError(f"Product_id: {item.product_id} not in cart")

        if item.quantity <= 0:
            cart_data.pop(item.product_id, None)
        else:
            cart_data[item.product_id] = item.quantity
        return cart_data

    async def remove_from_cart(
        self,
        cart_data: Dict[int, int],
        product_id: int,
        user: Optional[User] = None,
    ) -> Dict[int, int]:
        if user:
            stmt = delete(CartItemModel).where(
                CartItemModel.user_id == user.id,
                CartItemModel.product_id == product_id
            )
            await self.session.execute(stmt)
            await self.session.commit()
            return await self.get_user_cart_dict(user)

        cart_data.pop(product_id, None)
        return cart_data

    async def get_cart_details(
        self,
        cart_data: Dict[int, int],
        user: Optional[User] = None,
    ) -> CartResponse:
        effective_cart = cart_data
        if user:
            effective_cart = await self.get_user_cart_dict(user)

        if not effective_cart:
            return CartResponse(items=[], total=0.0, items_count=0)

        product_ids = list(effective_cart.keys())
        products = await self.product_service.get_multiple_products_by_ids(product_ids)
        products_dict = {p.id: p for p in products}

        cart_items = []
        total_price = total_items = 0

        for product_id, quantity in effective_cart.items():
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
            items=cart_items,
            total=round(total_price, 2),
            items_count=total_items,
            cart_dict=effective_cart
        )
