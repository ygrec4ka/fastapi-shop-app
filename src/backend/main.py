import logging
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse


from core.config import settings
from api import router as api_router
from core.exceptions import EntityNotFoundError


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
