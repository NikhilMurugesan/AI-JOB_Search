from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.resume import Resume
from app.schemas.resume import ResumeCreate


class ResumeRepository:
    def create(self, db: Session, payload: ResumeCreate) -> Resume:
        entity = Resume(**payload.model_dump())
        db.add(entity)
        db.commit()
        db.refresh(entity)
        return entity

    def list_all(self, db: Session) -> list[Resume]:
        return list(db.scalars(select(Resume).order_by(Resume.created_at.desc())))
