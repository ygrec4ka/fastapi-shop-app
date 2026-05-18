from fastapi import APIRouter, status, Depends
from pydantic import BaseModel

from backend.api.dependencies.cart import get_cart_service
from backend.core.config import settings
from backend.core.authentication.fastapi_users import current_active_user
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

class UpdateCartRequest(BaseModel):
    product_id: int
    quantity: int

@router.post("/add", status_code=status.HTTP_200_OK)
async def add_to_cart(
    request: AddToCartRequest,
    cart_service: CartService = Depends(get_cart_service),
    user: User = Depends(current_active_user),
):
    item = CartItemCreate(
        product_id=request.product_id,
        quantity=request.quantity,
    )
    await cart_service.add_to_cart(item, user)
    return {"status": "success"}

@router.get(
    "/",
    response_model=CartResponse,
    status_code=status.HTTP_200_OK,
)
async def get_cart(
    cart_service: CartService = Depends(get_cart_service),
    user: User = Depends(current_active_user),
):
    return await cart_service.get_cart_details(user)

@router.put("/update", status_code=status.HTTP_200_OK)
async def update_cart_item(
    request: UpdateCartRequest,
    cart_service: CartService = Depends(get_cart_service),
    user: User = Depends(current_active_user),
):
    item = CartItemUpdate(product_id=request.product_id, quantity=request.quantity)
    await cart_service.update_cart_item(item, user)
    return {"status": "success"}

@router.delete("/remove/{product_id}", status_code=status.HTTP_200_OK)
async def remove_from_cart(
    product_id: int,
    cart_service: CartService = Depends(get_cart_service),
    user: User = Depends(current_active_user),
):
    await cart_service.remove_from_cart(product_id, user)
    return {"status": "success"}
