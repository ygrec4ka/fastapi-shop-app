from typing import Annotated
from fastapi import Depends

from backend.core.authentication.strategy import get_database_strategy as core_get_strategy
from .access_token import get_access_tokens_db

async def get_database_strategy(
    access_token_db = Depends(get_access_tokens_db)
):
    return core_get_strategy(access_token_db)