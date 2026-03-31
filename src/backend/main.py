import sys
from pathlib import Path

import logging
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

SRC_DIR = Path(__file__).resolve().parent.parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from backend.core.config import settings
from backend.api import router as api_router
from backend.core.exceptions import EntityNotFoundError


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


@app.exception_handler(EntityNotFoundError)
async def entity_not_found_exception_handler(request, exc: EntityNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": exc.message},
    )


if __name__ == "__main__":
    uvicorn.run(
        "backend.main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
