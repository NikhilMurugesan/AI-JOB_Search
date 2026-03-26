# Frontend (Angular)

This folder now contains a production-style **Step 1 frontend foundation** using Angular standalone APIs.

## What is included in Step 1
- Angular app shell with routing.
- Dashboard page scaffold with:
  - summary cards
  - search/filter form
  - jobs table
- API service seam targeting backend `GET /api/v1/jobs`.
- Fallback demo jobs when backend is unavailable (useful for demos/interviews).

## Why this structure is interview-quality
- `core/` isolates shared models + API clients.
- `features/` keeps domain modules independent and scalable.
- Standalone Angular components reduce module boilerplate while staying production-friendly.

## Run frontend
```bash
cd frontend
npm install
npm run start
```

Open: http://localhost:4200

## Typecheck/build
```bash
cd frontend
npm run typecheck
npm run build
```

## Next step
Step 2 will add resume upload and full backend integration for real job ingestion + filtering.
