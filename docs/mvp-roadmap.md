# MVP Roadmap

## Phase 0 (Current): Foundation
- Monorepo structure
- FastAPI bootstrapping
- DB setup + first entity
- Health checks + basic tests

## Phase 1: Resume Ingestion
- Resume upload endpoint (txt/pdf placeholder)
- Resume parsing pipeline
- Persist normalized resume profile

## Phase 2: Job Search and Collection
- Job source adapter interfaces
- Add at least one public data source
- Persist jobs + deduplicate

## Phase 3: Matching + Ranking
- Rule-based baseline scorer
- LLM-assisted match justification
- Relevance score endpoint for UI sorting

## Phase 4: Material Generation
- Generate 5 resume variants
- Match best variant per job
- Generate cover letter + outreach draft

## Phase 5: Application Tracking + UI
- Full status pipeline
- Angular pages for dashboard, jobs, materials, filters

## Phase 6: Agentic Orchestration
- Tool registry + planner/executor
- Human-in-the-loop approval for final apply action

## Phase 7: Production Readiness
- Postgres migration
- Docker + CI + observability
