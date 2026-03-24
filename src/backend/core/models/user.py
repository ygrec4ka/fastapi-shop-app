from typing import TYPE_CHECKING, List

from sqlalchemy.orm import Mapped, relationship


from backend.core.models import Base
from backend.core.models.mixins.id_int_pk import IdIntPk
from backend.core.types import UserIdType

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from backend.core.config import AccessToken


class User(Base, IdIntPk, SQLAlchemyBaseUserTable[UserIdType]):

    access_tokens: Mapped[List["AccessToken"]] = relationship(
        "AccessToken", back_populates="user", cascade="all, delete-orphan"
    )

    @classmethod
    async def get_db(cls, session: "AsyncSession"):
        yield SQLAlchemyUserDatabase(session, cls)

    def __str__(self):
        return self.email