from fastapi import APIRouter

from app.config import settings


from .categories import router as categories_router
from .products import router as products_router
from .cart import router as cart_router

router = APIRouter(
    prefix=settings.api.v1.prefix,
)


router.include_router(categories_router)
router.include_router(products_router)
router.include_router(cart_router)
