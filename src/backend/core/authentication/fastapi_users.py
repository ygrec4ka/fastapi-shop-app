from fastapi_users import FastAPIUsers

from backend.api.dependencies.authentication.backend import authentication_backend
from backend.api.dependencies.authentication.user_manager import get_user_manager

from backend.core.types import UserIdType
from backend.core.models import User


fastapi_users = FastAPIUsers[User, UserIdType](
    get_user_manager,
    [authentication_backend],
)


optional_current_user = fastapi_users.current_user(optional=True)
current_active_user = fastapi_users.current_user(active=True)
current_active_superuser = fastapi_users.current_user(active=True, superuser=True)
