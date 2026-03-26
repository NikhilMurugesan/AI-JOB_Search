from sqlalchemy.orm import Session

from app.adapters.job_source import JobSourceAdapter
from app.adapters.remotive_adapter import RemotiveAdapter
from app.repositories.job_repository import JobRepository
from app.schemas.job import JobIngestResponse


class JobService:
    def __init__(
        self,
        repo: JobRepository | None = None,
        adapter: JobSourceAdapter | None = None,
    ) -> None:
        self.repo = repo or JobRepository()
        self.adapter = adapter or RemotiveAdapter()

    def ingest_jobs(self, db: Session, query: str, limit: int) -> JobIngestResponse:
        fetched_jobs = self.adapter.search_jobs(query=query, limit=limit)
        ingested_count, deduped_count = self.repo.create_many_dedup(db, fetched_jobs)
        return JobIngestResponse(
            source=self.adapter.source_name,
            fetched=len(fetched_jobs),
            ingested=ingested_count,
            deduplicated=deduped_count,
        )

    def list_jobs(self, db: Session):
        return self.repo.list_all(db)
