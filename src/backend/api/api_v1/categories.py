from typing import List

from fastapi import APIRouter, status, Depends

from backend.core.config import settings
from backend.api.dependencies.category import get_category_service
from backend.core.schemas.category import CategoryResponse
from backend.services.category import CategoryService


router = APIRouter(
    prefix=settings.api.v1.categories,
    tags=["Categories"],
)


@router.get(
    "/",
    response_model=List[CategoryResponse],
    status_code=status.HTTP_200_OK,
)
async def get_categories(
    category_service: CategoryService = Depends(get_category_service),
):
    return await category_service.get_all_categories()


@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
    status_code=status.HTTP_200_OK,
)
async def get_category(
    category_id: int,
    category_service: CategoryService = Depends(get_category_service),
):
    return await category_service.get_category_by_id(category_id)
