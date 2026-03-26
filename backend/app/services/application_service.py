import logging
from datetime import datetime

from sqlalchemy.orm import Session

from app.models.application import ApplicationStatus, JobApplication
from app.repositories.application_repository import ApplicationRepository
from app.schemas.application import (
    ApplicationCreate,
    ApplicationListResponse,
)
from app.utils.exceptions import ApplicationNotFoundError

logger = logging.getLogger(__name__)


class ApplicationService:
    def __init__(self, db: Session):
        self.repository = ApplicationRepository(db)

    def create_application(self, payload: ApplicationCreate) -> JobApplication:
        logger.info(
            "Creating application for company=%s role=%s",
            payload.company_name,
            payload.role_title,
        )

        application = JobApplication(
            company_name=payload.company_name,
            role_title=payload.role_title,
            job_description=payload.job_description,
            status=payload.status,
            match_score=payload.match_score,
        )

        if payload.status == ApplicationStatus.APPLIED:
            application.date_applied = datetime.utcnow()

        return self.repository.create(application)

    def list_applications(self) -> ApplicationListResponse:
        items = self.repository.list_all()
        total = self.repository.count_all()
        return ApplicationListResponse(items=items, total=total)

    def get_application(self, application_id: int) -> JobApplication:
        application = self.repository.get_by_id(application_id)
        if not application:
            raise ApplicationNotFoundError(application_id)
        return application

    def update_status(
        self, application_id: int, status: ApplicationStatus
    ) -> JobApplication:
        application = self.repository.get_by_id(application_id)
        if not application:
            raise ApplicationNotFoundError(application_id)

        application.status = status

        if status == ApplicationStatus.APPLIED and application.date_applied is None:
            application.date_applied = datetime.utcnow()

        logger.info(
            "Updating application id=%s to status=%s",
            application_id,
            status.value,
        )
        return self.repository.update(application)