# API

FastAPI exposes the versioned OpenAPI schema at `/openapi.json` and interactive documentation at `/docs`.

Key routes:

- `POST /api/v1/auth/register`, `/login`, `/logout`; session cookie authentication.
- `GET|POST /api/v1/workspaces`; user-owned research spaces.
- `POST /api/v1/workspaces/{workspace_id}/documents`; asynchronous PDF upload.
- `GET /api/v1/documents/{document_id}/status`; worker progress.
- `POST /api/v1/documents/{document_id}/retry`; safely creates a fresh processing job.
- `POST /api/v1/chat`; source-grounded response and persisted citations.
- `POST /api/v1/voice/transcribe`, `/voice/speak`; local speech endpoints.
