# Data flow

1. An authenticated user uploads a PDF to a workspace.
2. The API validates extension, content type, PDF magic bytes, size, and basename; it stores bytes in MinIO and creates a queued processing job.
3. Redis/ARQ sends only the document UUID to the worker.
4. The worker uses PyMuPDF native extraction, OCRs only low-quality pages, makes page-bound structure-aware chunks, persists provenance in PostgreSQL, embeds in batches, then writes vectors to Qdrant.
5. Only after indexing succeeds is the document marked `ready`.
6. Chat uses authorized workspace scope, compact recent memory, and retrieved evidence. Citation records link the assistant message to exact stored chunk and page metadata.

