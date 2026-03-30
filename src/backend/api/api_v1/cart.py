from typing import Dict, Optional

from fastapi import APIRouter, status, Depends

from pydantic import BaseModel

from backend.api.dependencies import get_cart_service
from backend.core.config import settings
from backend.api.dependencies.authentication.users import optional_current_user
from backend.core.models import User
from backend.core.schemas.cart import CartItemCreate, CartResponse, CartItemUpdate
from backend.services.cart import CartService


router = APIRouter(
    prefix=settings.api.v1.cart,
    tags=["Cart"],
)


class AddToCartRequest(BaseModel):
    product_id: int
    quantity: int
    cart: Dict[int, int] = {}


class UpdateCartRequest(AddToCartRequest):
    pass


class RemoveFromCartRequest(BaseModel):
    cart: Dict[int, int] = {}


@router.post("/add", status_code=status.HTTP_200_OK)
async def add_to_cart(
    request: AddToCartRequest,
    cart_service: CartService = Depends(get_cart_service),
    user: Optional[User] = Depends(optional_current_user),
):
    item = CartItemCreate(
        product_id=request.product_id,
        quantity=request.quantity,
    )
    updated_cart = await cart_service.add_to_cart(request.cart, item, user=user)

    return {"cart": updated_cart}


@router.post(
    "/cart",
    response_model=CartResponse,
    status_code=status.HTTP_200_OK,
)
async def get_cart(
    cart_data: Dict[int, int],
    cart_service: CartService = Depends(get_cart_service),
    user: Optional[User] = Depends(optional_current_user),
):

    return await cart_service.get_cart_details(cart_data, user=user)


@router.put("/update", status_code=status.HTTP_200_OK)
async def update_cart_item(
    request: UpdateCartRequest,
    cart_service: CartService = Depends(get_cart_service),
    user: Optional[User] = Depends(optional_current_user),
):
    item = CartItemUpdate(product_id=request.product_id, quantity=request.quantity)
    updated_cart = await cart_service.update_cart_item(request.cart, item, user=user)

    return {"cart": updated_cart}


@router.delete("/remove/{product_id}", status_code=status.HTTP_200_OK)
async def remove_from_cart(
    product_id: int,
    request: RemoveFromCartRequest,
    cart_service: CartService = Depends(get_cart_service),
    user: Optional[User] = Depends(optional_current_user),
):
    updated_cart = await cart_service.remove_from_cart(
        request.cart, product_id, user=user
    )

    return {"cart": updated_cart}
