# Backend Integration Notes

## Source

- Latest backend source was pulled from `https://github.com/TjandraD/cv-processor.git`.
- The backend lives in this project under `be/`.
- The model archive from the project root was moved to `be/models.zip`.
- `be/models.zip` extracts to `be/models/finetuned/`.

## Frontend Contract

The React frontend talks to the backend through `fe/src/api/client.ts`.

- `GET /api/jobs?limit=100`
  - Returns `status`, `total`, `page`, `limit`, and `jobs`.
  - Each job item must include `job_id`, `title`, `company`, `industry`, `required_experience_years`, and `created_at`.
- `GET /api/jobs/<job_id>`
  - Returns job detail with `job_id`, `title`, `company`, `industry`, `description`, `required_skills`, `required_experience_years`, `required_education`, and `created_at`.
- `POST /api/match`
  - Receives `job_id`, `candidate_id`, `candidate_name`, and pre-extracted `cv_text`.
  - Returns `job_id`, `job_title`, `candidate_id`, `candidate_name`, `language_detected`, `grade`, `score_comparison`, `breakdown`, and `processing_time_ms`.

## Auth And Runtime Wiring

- Backend auth is controlled by `APP_TOKEN` in `be/backend/.env`.
- The frontend sends `Authorization: Bearer <VITE_API_TOKEN>` when `VITE_API_TOKEN` is set.
- In Docker, `fe/nginx.conf` proxies `/api/` to the backend and injects `Authorization: Bearer ${APP_TOKEN}`.
- Root `docker-compose.yml` builds the backend from `./be` and the frontend from `./fe`.

## Model Loading

- The new backend expects the fine-tuned SentenceTransformer model at `models/finetuned`.
- For local runs from `be/backend`, that relative path would normally point to the wrong folder.
- `be/backend/config.py` now resolves relative model paths against the backend repo root (`be/`) when needed.
- Docker now copies `be/models.zip` and extracts it into `/app/models/finetuned` during image build.
- `be/models.zip` and extracted `be/models/` are ignored by git because they are large runtime artifacts.

## Files Most Affected By Future Backend Updates

- `be/backend/config.py`: local/Docker model path behavior.
- `be/Dockerfile`: model archive extraction and backend image build.
- `be/backend/routes/jobs.py`: frontend job list/detail response contract.
- `be/backend/routes/match.py`: frontend match response contract.
- `be/backend/seed/jobs_seed.sql`: job data shown in the frontend.
- `docker-compose.yml`: project-level frontend/backend service wiring.
- `fe/nginx.conf`: Docker API proxy and auth header injection.
- `fe/src/api/client.ts`: frontend API types and request paths.
