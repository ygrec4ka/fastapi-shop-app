import logging

import uvicorn
from fastapi import FastAPI

from app.config import settings
from api import router as api_router

logging.basicConfig(
    level=settings.logging.log_level_value,
    format=settings.logging.log_format,
)


app = FastAPI()


app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
