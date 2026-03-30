from fastapi import APIRouter, Depends, status

from backend.api.dependencies import get_product_service
from backend.core.config import settings
from backend.core.schemas.product import ProductListResponse, ProductResponse
from backend.services.product import ProductService

router = APIRouter(
    prefix=settings.api.v1.products,
    tags=["Products"],
)


@router.get(
    "/",
    response_model=ProductListResponse,
    status_code=status.HTTP_200_OK,
)
async def get_products(
    product_service: ProductService = Depends(get_product_service),
):
    products = await product_service.get_all_products()
    return {
        "items": products,
        "total": len(products),
    }


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK,
)
async def get_product(
    product_id: int,
    product_service: ProductService = Depends(get_product_service),
):
    return await product_service.get_product_by_id(product_id)


@router.get(
    "/category/{category_id}",
    response_model=ProductListResponse,
    status_code=status.HTTP_200_OK,
)
async def get_products_by_category(
    category_id: int,
    product_service: ProductService = Depends(get_product_service),
):
    products = await product_service.get_products_by_category(category_id)
    return {
        "items": products,
        "total": len(products),
    }
