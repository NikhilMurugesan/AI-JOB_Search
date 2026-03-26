from datetime import datetime, timezone

from fastapi.testclient import TestClient

from app.adapters.job_source import ExternalJob
from app.api.v1.jobs import get_job_service
from app.main import app
from app.services.job_service import JobService

client = TestClient(app)


class FakeAdapter:
    source_name = "fake-public"

    def search_jobs(self, query: str, limit: int) -> list[ExternalJob]:
        return [
            ExternalJob(
                source=self.source_name,
                source_job_id="fp-1",
                title="Python Backend Engineer",
                company="Acme",
                location="Remote US",
                url="https://example.com/jobs/fp-1",
                description=f"{query} role 1",
                posted_at=datetime.now(timezone.utc),
            ),
            ExternalJob(
                source=self.source_name,
                source_job_id="fp-2",
                title="AI Engineer",
                company="Globex",
                location="Remote",
                url="https://example.com/jobs/fp-2",
                description=f"{query} role 2",
                posted_at=datetime.now(timezone.utc),
            ),
        ][:limit]


def test_ingest_and_deduplicate_jobs() -> None:
    app.dependency_overrides[get_job_service] = lambda: JobService(adapter=FakeAdapter())

    payload = {"query": "python", "limit": 10}
    first = client.post("/api/v1/jobs/ingest", json=payload)
    assert first.status_code == 200
    assert first.json()["ingested"] == 2
    assert first.json()["deduplicated"] == 0

    second = client.post("/api/v1/jobs/ingest", json=payload)
    assert second.status_code == 200
    assert second.json()["ingested"] == 0
    assert second.json()["deduplicated"] == 2

    listed = client.get("/api/v1/jobs")
    assert listed.status_code == 200
    assert len([item for item in listed.json() if item["source"] == "fake-public"]) >= 2

    app.dependency_overrides.clear()
