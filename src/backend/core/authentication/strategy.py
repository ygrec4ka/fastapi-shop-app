from fastapi_users.authentication.strategy import DatabaseStrategy

from backend.core.config import settings


def get_database_strategy(access_token_db) -> DatabaseStrategy:
    return DatabaseStrategy(
        database=access_token_db,
        lifetime_seconds=settings.access_token.lifetime_seconds,
    )
