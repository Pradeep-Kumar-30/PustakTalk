# Local development

Prerequisites: Docker Engine with Docker Compose v2.24+, Node 22+, Python 3.11–3.14, and local Ollama. This repository does not bundle model weights.

```sh
cp .env.example .env
make setup
make up
```

Open `http://localhost:3000`. The API OpenAPI document is at `http://localhost:8000/docs`.

`make setup` creates `.venv` in the repository and installs both the API and document-worker packages there. `make up` waits for the local services to become ready. To stop them, run `make down`.

The default first run is intentionally a lightweight core stack. Once it is
healthy, run `ollama pull qwen3:0.6b`, set `INSTALL_AI=true` in `.env`, and run
`make up` again to install local embedding and speech providers. This avoids a
large model-runtime download blocking the first UI/API launch on slow networks.

For the complete RAG and voice profile, use a machine with at least 16 GiB RAM.
The API and worker persist downloaded Hugging Face models in `model-cache`; Piper
voice files persist in `piper-voices`. Download the selected, licence-approved
Piper voices into `PIPER_DATA_DIR` after the AI images are running.

Before the first start, set a non-default `AUTH_SECRET` in `.env`. If you change the database credentials, keep `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, and `DATABASE_URL` aligned. If you change MinIO credentials, update `MINIO_ACCESS_KEY` and `MINIO_SECRET_KEY`; Compose applies those same values to the MinIO server. Existing PostgreSQL and MinIO volumes retain their original initialization credentials, so credential rotation is a separate maintenance operation.

## VS Code

Open the repository folder in VS Code, install the Python, Pylance, Tailwind CSS IntelliSense, and Docker extensions, then choose the `.venv/bin/python` interpreter if VS Code does not select it automatically. Use **Terminal → Run Task** and select **PustakTalk: setup** once, then **PustakTalk: start stack**. The task starts the complete Docker stack; use the integrated terminal for `ollama pull qwen3:0.6b` before uploading or chatting with a document.

The current development machine has 5.7 GiB RAM and no CUDA GPU. Keep `ENABLE_RERANKER=false`, use CPU `int8` Whisper, and avoid processing many PDFs concurrently. Download a multilingual SentenceTransformer model before the first worker job if the worker cannot access Hugging Face at runtime.

For a stronger local experience, use at least 16 GiB RAM and set `LLM_MODEL=qwen3:1.7b` after measuring end-to-end latency. Do not expose MinIO, Qdrant, Redis, or PostgreSQL ports publicly.
