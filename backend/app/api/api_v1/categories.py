from typing import List

from fastapi import APIRouter
from fastapi.params import Depends
from starlette import status

from app.config import settings

from app.api.dependencies import get_category_services
from app.core.schemas.category import CategoryResponse
from app.core.services.category import CategoryService

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
    category_service: CategoryService = Depends(get_category_services),
):
    return await category_service.get_all_categories()


@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
    status_code=status.HTTP_200_OK,
)
async def get_category(
    category_id: int,
    category_service: CategoryService = Depends(get_category_services),
):
    return await category_service.get_category_by_id(category_id)
