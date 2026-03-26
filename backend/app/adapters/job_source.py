from dataclasses import dataclass
from datetime import datetime
from typing import Protocol


@dataclass
class ExternalJob:
    source: str
    source_job_id: str
    title: str
    company: str
    location: str
    url: str
    description: str
    posted_at: datetime | None = None


class JobSourceAdapter(Protocol):
    source_name: str

    def search_jobs(self, query: str, limit: int) -> list[ExternalJob]:
        ...
