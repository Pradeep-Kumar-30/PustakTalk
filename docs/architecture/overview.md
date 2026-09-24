# Architecture overview

PustakTalk is a modular monorepo with independently deployable web, API, and worker processes. The browser never talks directly to a model, vector database, or object store.

```text
Browser → Next.js → FastAPI → PostgreSQL / Redis / MinIO / Qdrant
                              ↓
                         document worker → local embeddings → Qdrant
                              ↓
                   local Ollama / faster-whisper / Piper TTS
```

The API owns authorization and small transactional commands. The worker owns parsing, OCR, chunking, embedding, and indexing. This keeps PDF upload latency bounded even for large files.

## Boundaries

- `modules/` owns HTTP schemas, services, repositories, and SQL models by product feature.
- `ai/` depends on replaceable provider interfaces, rather than an Ollama or Qdrant implementation.
- `document_processing/` contains deterministic provenance-preserving transformations.
- `infrastructure/` adapts external databases, queues, storage, and vector search.
- The frontend puts calls, feature state, and rendering in separate feature folders.

## Security boundary

Identity comes from the signed HTTP-only cookie, not a client-provided user ID. Every workspace and document read checks ownership. PDF text is passed to prompts in a labelled evidence region and is never treated as executable instructions.

