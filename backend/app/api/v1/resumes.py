from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.resume import ResumeCreate, ResumeRead
from app.services.resume_service import ResumeService

router = APIRouter(prefix="/resumes", tags=["resumes"])


@router.post("", response_model=ResumeRead, status_code=status.HTTP_201_CREATED)
def create_resume(payload: ResumeCreate, db: Session = Depends(get_db)):
    service = ResumeService()
    return service.create_resume(db, payload)


@router.get("", response_model=list[ResumeRead])
def list_resumes(db: Session = Depends(get_db)):
    service = ResumeService()
    return service.list_resumes(db)
