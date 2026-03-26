from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.logging import setup_logging
from app.db.base import Base
from app.db.session import engine
from app.models.job import Job  # noqa: F401
from app.models.resume import Resume  # noqa: F401

setup_logging()
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)
app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "AI Job Search Copilot API running"}
