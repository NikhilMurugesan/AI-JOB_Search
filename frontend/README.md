# Frontend (Angular)

Step 1 keeps frontend lightweight but structured.

## Recommended bootstrap command
```bash
cd frontend
npx @angular/cli@latest new web --standalone --routing --style=scss
```

Then map generated app into this planned structure:
- `src/app/core` for API clients, interceptors, config
- `src/app/features/jobs` for jobs dashboard and details
- `src/app/features/resumes` for upload/variants
- `src/app/features/applications` for pipeline tracking
- `src/app/shared` reusable UI components

In Step 2 we will wire real components to backend endpoints.
