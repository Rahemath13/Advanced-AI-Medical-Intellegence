from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.history import router as history_router
from app.api.routes.prediction import router as prediction_router
from app.core.config import get_settings
from app.database.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize application resources."""
    init_db()
    yield


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "End-to-end AI medical image analysis platform "
        "with deep learning, Grad-CAM, LLM reporting, "
        "REST API, and prediction history."
    ),
    lifespan=lifespan,
)

app.include_router(health_router)
app.include_router(prediction_router)
app.include_router(history_router)

@app.get("/", tags=["System"])
def root() -> dict:
    """Return basic application information."""
    return {
        "application": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "docs": "/docs",
        "health": "/health",
    }