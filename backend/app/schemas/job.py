from datetime import datetime

from pydantic import BaseModel, Field


class JobIngestRequest(BaseModel):
    query: str = Field(min_length=2, max_length=120)
    limit: int = Field(default=20, ge=1, le=100)


class JobRead(BaseModel):
    id: int
    source: str
    source_job_id: str
    title: str
    company: str
    location: str
    url: str
    description: str
    posted_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}


class JobIngestResponse(BaseModel):
    source: str
    fetched: int
    ingested: int
    deduplicated: int
