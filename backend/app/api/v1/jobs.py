from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.job import JobIngestRequest, JobIngestResponse, JobRead
from app.services.job_service import JobService

router = APIRouter(prefix="/jobs", tags=["jobs"])


def get_job_service() -> JobService:
    return JobService()


@router.post("/ingest", response_model=JobIngestResponse, status_code=status.HTTP_200_OK)
def ingest_jobs(
    payload: JobIngestRequest,
    db: Session = Depends(get_db),
    service: JobService = Depends(get_job_service),
):
    return service.ingest_jobs(db=db, query=payload.query, limit=payload.limit)


@router.get("", response_model=list[JobRead])
def list_jobs(
    db: Session = Depends(get_db),
    service: JobService = Depends(get_job_service),
):
    return service.list_jobs(db)
