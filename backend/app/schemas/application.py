from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models.application import ApplicationStatus


class ApplicationBase(BaseModel):
    company_name: str = Field(..., min_length=1, max_length=255)
    role_title: str = Field(..., min_length=1, max_length=255)
    job_description: str = Field(..., min_length=20)
    status: ApplicationStatus = ApplicationStatus.DRAFT
    match_score: Optional[float] = Field(default=None, ge=0, le=100)


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationUpdateStatus(BaseModel):
    status: ApplicationStatus


class ApplicationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company_name: str
    role_title: str
    job_description: str
    status: ApplicationStatus
    match_score: Optional[float] = None
    tailored_resume: Optional[str] = None
    cover_letter: Optional[str] = None
    email_draft: Optional[str] = None
    jd_analysis: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    date_applied: Optional[datetime] = None


class ApplicationListResponse(BaseModel):
    items: list[ApplicationResponse]
    total: int