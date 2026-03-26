from datetime import datetime

import httpx

from app.adapters.job_source import ExternalJob


class RemotiveAdapter:
    """Public jobs source adapter using Remotive's remote jobs API."""

    source_name = "remotive"
    base_url = "https://remotive.com/api/remote-jobs"

    def search_jobs(self, query: str, limit: int) -> list[ExternalJob]:
        response = httpx.get(self.base_url, params={"search": query}, timeout=15)
        response.raise_for_status()

        jobs: list[ExternalJob] = []
        for raw in response.json().get("jobs", [])[:limit]:
            publication_date = raw.get("publication_date")
            posted_at = datetime.fromisoformat(publication_date) if publication_date else None
            jobs.append(
                ExternalJob(
                    source=self.source_name,
                    source_job_id=str(raw["id"]),
                    title=raw.get("title", ""),
                    company=raw.get("company_name", "Unknown"),
                    location=raw.get("candidate_required_location", "Remote"),
                    url=raw.get("url", ""),
                    description=raw.get("description", ""),
                    posted_at=posted_at,
                )
            )

        return jobs
