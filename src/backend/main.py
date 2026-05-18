import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from backend.core.config import settings
from backend.api import router as api_router


logging.basicConfig(
    level=settings.logging.log_level_value,
    format=settings.logging.log_format,
)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
