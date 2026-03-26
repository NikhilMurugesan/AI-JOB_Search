import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.application import (
    ApplicationCreate,
    ApplicationListResponse,
    ApplicationResponse,
    ApplicationUpdateStatus,
)
from app.services.application_service import ApplicationService
from app.utils.exceptions import ApplicationNotFoundError

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/applications", tags=["Applications"])


@router.post("", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
def create_application(
    payload: ApplicationCreate,
    db: Session = Depends(get_db),
):
    service = ApplicationService(db)
    return service.create_application(payload)


@router.get("", response_model=ApplicationListResponse)
def list_applications(
    db: Session = Depends(get_db),
):
    service = ApplicationService(db)
    return service.list_applications()


@router.get("/{application_id}", response_model=ApplicationResponse)
def get_application(
    application_id: int,
    db: Session = Depends(get_db),
):
    service = ApplicationService(db)
    try:
        return service.get_application(application_id)
    except ApplicationNotFoundError as exc:
        logger.warning(str(exc))
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.patch("/{application_id}/status", response_model=ApplicationResponse)
def update_application_status(
    application_id: int,
    payload: ApplicationUpdateStatus,
    db: Session = Depends(get_db),
):
    service = ApplicationService(db)
    try:
        return service.update_status(application_id, payload.status)
    except ApplicationNotFoundError as exc:
        logger.warning(str(exc))
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc