from datetime import datetime

from pydantic import BaseModel, Field


class ResumeCreate(BaseModel):
    title: str = Field(min_length=2, max_length=120)
    target_title: str | None = Field(default=None, min_length=2, max_length=200)
    target_location: str | None = Field(default=None, min_length=2, max_length=120)
    raw_text: str = Field(min_length=30)


class ResumeRead(BaseModel):
    id: int
    title: str
    target_title: str | None
    target_location: str | None
    raw_text: str
    created_at: datetime

    model_config = {"from_attributes": True}
