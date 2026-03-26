# AI Job Search Copilot

A production-style full-stack project scaffold for an AI-powered job search assistant.

## Tech Stack
- **Backend:** FastAPI + SQLAlchemy + SQLite (PostgreSQL-ready)
- **Frontend:** Angular standalone architecture (`frontend/`)
- **LLM:** OpenAI-compatible client abstraction

## Step 1 Scope
- Establish architecture and folder structure
- Create a runnable backend service with:
  - health endpoint
  - config management
  - database setup
  - base domain model (`Resume`)
  - versioned API routing
- Create a runnable frontend shell with dashboard scaffold and API service seam

## Run backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Open:
- API docs: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/api/v1/health

## Run frontend
```bash
cd frontend
npm install
npm run start
```

Open:
- UI: http://localhost:4200

## Test backend
```bash
cd backend
pytest -q
```
