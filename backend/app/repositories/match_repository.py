from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.job import Job
from app.models.resume import Resume


class MatchRepository:
    def get_resume(self, db: Session, resume_id: int) -> Resume | None:
        return db.scalar(select(Resume).where(Resume.id == resume_id))

    def list_jobs(self, db: Session) -> list[Job]:
        return list(db.scalars(select(Job).order_by(Job.created_at.desc(), Job.id.desc())))
