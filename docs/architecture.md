# AI Job Search Copilot - Architecture (Interview-Ready)

## High-Level Architecture

```text
[Angular UI]
   |
   | REST (JSON)
   v
[FastAPI Backend]
   |-- API Layer (routers)
   |-- Service Layer (business logic)
   |-- Repository Layer (DB operations)
   |-- AI Layer (LLM clients + prompts + structured outputs)
   |-- Agent Layer (tool orchestration, later)
   v
[SQLite -> PostgreSQL]
```

## Why this is good for interviews
- Clear separation of concerns (router/service/repository) demonstrates production thinking.
- Versioned APIs (`/api/v1`) show maintainability.
- DB abstraction eases SQLite to PostgreSQL migration.
- Prompts stored outside route handlers shows clean AI engineering practices.
- Agent layer planned as orchestrator demonstrates extensibility.

## Planned Modules
1. Resume upload + parse
2. Job ingestion/search adapters
3. Relevance scoring + ranking
4. Resume variant generation (5 role-targeted variants)
5. Resume-job matching
6. Cover letter + outreach generation
7. Application tracking pipeline
8. Dashboard + filters
9. Agent orchestration with human approval checkpoint

## Agent Tool Contract (future)
- `job_search_tool`
- `resume_variant_tool`
- `resume_match_tool`
- `cover_letter_tool`
- `email_draft_tool`
- `application_tracker_tool`

All tools will return structured JSON schemas for deterministic orchestration.
