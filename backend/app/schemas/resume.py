from datetime import datetime

from pydantic import BaseModel, Field


class ResumeCreate(BaseModel):
    title: str = Field(min_length=2, max_length=120)
    raw_text: str = Field(min_length=30)


class ResumeRead(BaseModel):
    id: int
    title: str
    raw_text: str
    created_at: datetime

    model_config = {"from_attributes": True}
