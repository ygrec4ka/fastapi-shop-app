import logging
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.core.config import settings
from backend.api import router as api_router


logging.basicConfig(
    level=settings.logging.log_level_value,
    format=settings.logging.log_format,
)


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to fastapi shop API",
    }


@app.get("/")
def health_check():
    return {"message": "OK"}


if __name__ == "__main__":
    uvicorn.run(
        "backend.main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
