# PustakTalk

**अपनी किताबों से बात कीजिए।**

Talk to your documents. Find answers. Hear them. See the source.

PustakTalk is a self-hostable, page-aware AI research workspace for PDFs, books, notes, and papers. It supports Hindi, English, and Hinglish questions while preserving the evidence behind each answer.

> Status: the repository provides a runnable local architecture and vertical slice. Production deployment is deliberately not claimed: it requires a server, domain, TLS, model/voice licence approval, and real acceptance testing with customer PDFs.

## Why PustakTalk?

Most PDF chat interfaces give a plausible answer and hide the trail. PustakTalk stores physical-page provenance through extraction, chunks, search, answers, citations, and the viewer. Page numbers are selected from stored metadata, never authored by a model.

## Features

- HTTP-only authentication cookies, user-owned workspaces, validation, and source-scoped authorization.
- Asynchronous PDF ingestion with PyMuPDF extraction, selective Tesseract OCR, structure-aware page chunks, MinIO, Redis/ARQ, PostgreSQL, and Qdrant.
- Hybrid lexical/dense retrieval, RRF fusion, optional local reranking, LangGraph intent routing, compact memory, citation validation, and groundedness signal.
- Clickable citation chips that open the cited PDF page and show the stored source excerpt.
- Browser microphone capture, faster-whisper transcription, local Piper TTS, and audio interruption/new-turn control.
- Local-model abstraction: Ollama, SentenceTransformers, faster-whisper, and Piper are replaceable providers—not hard-coded cloud APIs.

## Architecture

```text
apps/web → apps/api → PostgreSQL / Redis / MinIO / Qdrant
                       ↓
               workers/document-worker → embeddings / Ollama / speech
```

See [architecture overview](docs/architecture/overview.md), [RAG design](docs/architecture/rag.md), [voice design](docs/architecture/voice.md), and [data flow](docs/architecture/data-flow.md).

## Repository structure

```text
apps/                 Next.js browser and FastAPI API
workers/              asynchronous document worker
packages/contracts/   generated/shared API contract boundary
infrastructure/       Compose, Nginx, scripts, monitoring home
evaluation/           datasets, metrics, reproducible runner
tests/e2e/            full-stack acceptance test specification
docs/                 architecture, API, deployment, ADRs
```

## Technology choices

FastAPI and Next.js provide typed server/browser boundaries. PostgreSQL is the transactional source of truth, MinIO retains PDF binaries, Redis carries short-lived job state, and Qdrant indexes embeddings. Ollama exposes a local model API. The default low-memory profile uses `qwen3:0.6b`; Qwen3's official library lists 0.6B, 1.7B, and larger variants and states broad multilingual support. BGE-M3 is a larger multilingual alternative for appropriate hardware.

The current development machine has 5.7 GiB RAM and no detected GPU, so `ENABLE_RERANKER=false` and CPU INT8 Whisper are the sane defaults. Read [local deployment](docs/deployment/local.md) before selecting larger models.

## Quick start

```sh
cp .env.example .env
make setup
make up
```

Open `http://localhost:3000`; API documentation is at `http://localhost:8000/docs`.

The first start intentionally launches the core stack without downloading large
local embedding and speech packages. After it is healthy, run `ollama pull
qwen3:0.6b`, set `INSTALL_AI=true` in `.env`, then run `make up` again to enable
local RAG and voice processing.

For a production-quality local-model profile, use a 16 GiB+ Linux host. The
deployment guide covers private Ollama networking, persistent model caches, and
Piper voice provisioning.

## Configuration

All configuration is documented in `.env.example`. Keep secrets only in the untracked `.env`: `AUTH_SECRET`, database credentials, storage credentials, and any deployment credentials. Do not put model weights or secrets in Git.

For a fresh local volume, keep `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, and `DATABASE_URL` aligned. Compose passes `MINIO_ACCESS_KEY` and `MINIO_SECRET_KEY` to both the application and MinIO so a credential change remains consistent. Existing data volumes retain their original initialization credentials.

## Local AI models

`EMBEDDING_MODEL` defaults to a smaller multilingual E5 profile. BGE-M3 is a MIT-licensed multilingual 1024-dimensional alternative with a longer context window, but it needs more memory. `faster-whisper` is MIT licensed and supports CPU INT8. Piper is behind a provider interface; its active engine is GPL-3.0 and individual voice licences must be checked before production use.

## API, testing, and evaluation

The versioned API is described in [docs/api](docs/api/README.md). Use:

```sh
make lint
make test
make eval
```

`make eval` writes an explicit report without pretending that fixture data proves production RAG quality. Seed a representative document corpus and curated page/answer labels before using retrieval or citation scores as a release gate.

## Docker and deployment

`docker-compose.yml` is the local full stack. `docker-compose.prod.yml` adds Nginx and strips service port exposure. Ollama intentionally remains host-configured for GPU compatibility. Full instructions and acceptance gates are in [production deployment](docs/deployment/production.md).

## Security and limitations

PDF text is untrusted evidence. The prompt boundary forbids it from becoming instructions; citations originate from database chunks. Current limitations: real-time streaming STT is not implemented, native PDF viewer search/highlight is represented by page navigation plus source excerpt rather than text-layer annotation, and production rollout awaits actual infrastructure credentials and acceptance testing.

## Roadmap

- Add text-layer PDF rendering and bbox overlay highlights.
- Add workspace collaboration/membership roles and user preferences UI.
- Add streaming chat/SSE and incremental STT.
- Calibrate model, reranker, and chunking thresholds with labelled Hindi/Hinglish evaluations.
