from datetime import datetime, timezone

from fastapi.testclient import TestClient

from app.adapters.job_source import ExternalJob
from app.api.v1.jobs import get_job_service
from app.main import app
from app.services.job_service import JobService

client = TestClient(app)


class RankingAdapter:
    source_name = "rank-fixture"

    def search_jobs(self, query: str, limit: int) -> list[ExternalJob]:
        jobs = [
            ExternalJob(
                source=self.source_name,
                source_job_id="r-1",
                title="Senior Python Backend Engineer",
                company="Acme",
                location="Remote",
                url="https://example.com/jobs/r-1",
                description="Python FastAPI SQL AWS role building APIs",
                posted_at=datetime.now(timezone.utc),
            ),
            ExternalJob(
                source=self.source_name,
                source_job_id="r-2",
                title="Frontend React Engineer",
                company="Globex",
                location="New York, NY",
                url="https://example.com/jobs/r-2",
                description="React TypeScript UI engineering",
                posted_at=datetime.now(timezone.utc),
            ),
        ]
        return jobs[:limit]


def test_ranked_matches_for_resume() -> None:
    app.dependency_overrides[get_job_service] = lambda: JobService(adapter=RankingAdapter())

    ingest_res = client.post("/api/v1/jobs/ingest", json={"query": "python", "limit": 10})
    assert ingest_res.status_code == 200

    resume_res = client.post(
        "/api/v1/resumes",
        json={
            "title": "Backend Engineer",
            "target_title": "Python Backend Engineer",
            "target_location": "Remote",
            "raw_text": "Python FastAPI SQL AWS backend engineer with API platform experience.",
        },
    )
    assert resume_res.status_code == 201
    resume_id = resume_res.json()["id"]

    match_res = client.get(
        f"/api/v1/matches?resume_id={resume_id}&include_justification_template=true"
    )
    assert match_res.status_code == 200

    body = match_res.json()
    assert body["resume_id"] == resume_id
    assert body["total_jobs_evaluated"] >= 2
    assert len(body["results"]) >= 2

    first = body["results"][0]
    second = body["results"][1]

    assert first["rank"] == 1
    assert second["rank"] == 2
    assert first["total_score"] >= second["total_score"]
    assert first["job"]["source_job_id"] == "r-1"
    assert "python" in first["matched_skills"]
    assert first["justification_scaffold"]["prompt_template"]
    assert "summary" in first["justification_scaffold"]["expected_response_schema"]

    app.dependency_overrides.clear()


def test_ranked_matches_resume_not_found() -> None:
    response = client.get("/api/v1/matches?resume_id=999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Resume not found"
