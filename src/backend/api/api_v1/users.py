from fastapi import APIRouter

from backend.api.dependencies.authentication.fastapi_users import fastapi_users
from backend.core.config import settings
from backend.core.schemas.user import UserRead, UserUpdate

router = APIRouter(prefix=settings.api.v1.users, tags=["Users"])


router.include_router(
    router=fastapi_users.get_users_router(
        UserRead,
        UserUpdate,
    ),
)
