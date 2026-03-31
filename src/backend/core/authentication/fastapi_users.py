from fastapi_users import FastAPIUsers

from backend.core.models import User
from backend.core.types.user_id import UserIdType

from backend.api.dependencies.authentication import get_user_manager
from backend.api.dependencies.authentication import authentication_backend


fastapi_users = FastAPIUsers[User, UserIdType](
    get_user_manager,
    [authentication_backend],
)
