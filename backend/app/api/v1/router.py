from fastapi import APIRouter

from app.api.v1.health import router as health_router
from app.api.v1.jobs import router as jobs_router
from app.api.v1.resumes import router as resumes_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(jobs_router)
api_router.include_router(resumes_router)
