from typing import Dict

from fastapi import APIRouter
from fastapi.params import Depends
from pydantic import BaseModel
from starlette import status

from app.api.dependencies import get_cart_service
from app.config import settings
from app.core.schemas.cart import CartItemCreate, CartResponse, CartItemUpdate
from app.core.services.cart import CartService

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
):
    item = CartItemCreate(
        product_id=request.product_id,
        quantity=request.quantity,
    )
    updated_cart = cart_service.add_to_cart(request.cart, item)

    return {"cart": updated_cart}


@router.get(
    "/cart",
    response_model=CartResponse,
    status_code=status.HTTP_200_OK,
)
async def get_cart(
    cart_data: Dict[int, int],
    cart_service: CartService = Depends(get_cart_service),
):

    return cart_service.get_cart_details(cart_data)


@router.put("/update", status_code=status.HTTP_200_OK)
async def update_cart_item(
    request: UpdateCartRequest,
    cart_service: CartService = Depends(get_cart_service),
):
    item = CartItemUpdate(product_id=request.product_id, quantity=request.quantity)
    updated_cart = cart_service.update_cart_item(request.cart, item)

    return {"cart": updated_cart}


@router.delete("/remove/{product_id}", status_code=status.HTTP_200_OK)
async def remove_from_cart(
    product_id: int,
    request: RemoveFromCartRequest,
    cart_service: CartService = Depends(get_cart_service),
):
    updated_cart = cart_service.remove_from_cart(request.cart, product_id)

    return {"cart": updated_cart}
