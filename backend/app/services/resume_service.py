from sqlalchemy.orm import Session

from app.repositories.resume_repository import ResumeRepository
from app.schemas.resume import ResumeCreate


class ResumeService:
    def __init__(self, repo: ResumeRepository | None = None) -> None:
        self.repo = repo or ResumeRepository()

    def create_resume(self, db: Session, payload: ResumeCreate):
        return self.repo.create(db, payload)

    def list_resumes(self, db: Session):
        return self.repo.list_all(db)
