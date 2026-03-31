from fastapi import APIRouter

from backend.core import settings
from backend.core.schemas.user import UserRead, UserCreate
from backend.api.dependencies.authentication import authentication_backend
from backend.core.authentication import fastapi_users

router = APIRouter(
    prefix=settings.api.v1.auth,
    tags=["Auth"],
)


router.include_router(
    router=fastapi_users.get_auth_router(
        authentication_backend,
    ),
)


router.include_router(
    router=fastapi_users.get_register_router(
        UserRead,
        UserCreate,
    ),
)
