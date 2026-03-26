from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_and_list_resumes() -> None:
    payload = {
        "title": "Base Resume",
        "raw_text": "Experienced AI engineer with production ML systems and LLM integration expertise.",
    }
    create_res = client.post("/api/v1/resumes", json=payload)
    assert create_res.status_code == 201

    list_res = client.get("/api/v1/resumes")
    assert list_res.status_code == 200
    assert len(list_res.json()) >= 1
