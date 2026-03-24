from fastapi import APIRouter

from backend.core.config import settings


from .auth import router as auth_router
from .users import router as users_router
from .categories import router as categories_router
from .products import router as products_router
from .cart import router as cart_router


router = APIRouter(
    prefix=settings.api.v1.prefix,
)


router.include_router(users_router)
router.include_router(auth_router)
router.include_router(categories_router)
router.include_router(products_router)
router.include_router(cart_router)