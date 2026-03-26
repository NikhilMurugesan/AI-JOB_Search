from sqlalchemy import select, tuple_
from sqlalchemy.orm import Session

from app.adapters.job_source import ExternalJob
from app.models.job import Job


class JobRepository:
    def list_all(self, db: Session) -> list[Job]:
        return list(db.scalars(select(Job).order_by(Job.created_at.desc())))

    def create_many_dedup(self, db: Session, jobs: list[ExternalJob]) -> tuple[int, int]:
        if not jobs:
            return 0, 0

        keys = {(job.source, job.source_job_id) for job in jobs}
        existing = set(
            db.execute(
                select(Job.source, Job.source_job_id).where(tuple_(Job.source, Job.source_job_id).in_(list(keys)))
            ).all()
        )

        to_insert = [
            Job(
                source=job.source,
                source_job_id=job.source_job_id,
                title=job.title,
                company=job.company,
                location=job.location,
                url=job.url,
                description=job.description,
                posted_at=job.posted_at,
            )
            for job in jobs
            if (job.source, job.source_job_id) not in existing
        ]

        db.add_all(to_insert)
        db.commit()

        return len(to_insert), len(jobs) - len(to_insert)
