from typing import Annotated, TYPE_CHECKING

from fastapi import Depends

from backend.core.models import db_helper, User
from backend.core.authentication.fastapi_users import fastapi_users

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_users_db(
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
):
    async for db in User.get_db(session=session):
        yield db


optional_current_user = fastapi_users.current_user(optional=True)
