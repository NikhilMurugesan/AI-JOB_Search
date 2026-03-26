from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.models.application import JobApplication


class ApplicationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, application: JobApplication) -> JobApplication:
        self.db.add(application)
        self.db.commit()
        self.db.refresh(application)
        return application

    def get_by_id(self, application_id: int) -> JobApplication | None:
        stmt = select(JobApplication).where(JobApplication.id == application_id)
        return self.db.execute(stmt).scalar_one_or_none()

    def list_all(self) -> list[JobApplication]:
        stmt = select(JobApplication).order_by(desc(JobApplication.created_at))
        return list(self.db.execute(stmt).scalars().all())

    def count_all(self) -> int:
        return len(self.list_all())

    def update(self, application: JobApplication) -> JobApplication:
        self.db.add(application)
        self.db.commit()
        self.db.refresh(application)
        return application