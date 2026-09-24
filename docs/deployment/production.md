# Production deployment

Provision a Linux server and measure CPU, RAM, disk, GPU, and VRAM before choosing any model. Populate a private `.env` with high-entropy secrets; do not use the example MinIO or authentication values.

```sh
./infrastructure/scripts/deploy.sh
```

The deploy script waits for services, applies Alembic migrations, and verifies the Nginx-routed API and web application. The production Compose overlay forces `APP_ENV=production`, secure auth cookies, and removes every host port except Nginx on port 80. Set high-entropy `AUTH_SECRET`, storage/database credentials, explicit `CORS_ORIGINS`, and backup/firewall settings in the private `.env`. Place Nginx/Caddy behind TLS. The production Compose file intentionally does not containerize Ollama: GPU driver/runtime choices vary by host. Point `OLLAMA_BASE_URL` at the validated local inference service instead.

## Local AI preflight

Use a Linux server with at least 16 GiB RAM for the RAG and voice profile; a GPU is optional. Keep the Ollama listener private to the server and Docker bridge—never expose port 11434 publicly. Configure its service with `OLLAMA_HOST=0.0.0.0:11434`, restrict that port in the host firewall, pull the configured `LLM_MODEL`, and set `INSTALL_AI=true` in the private `.env` before deploying.

The API and worker persist Hugging Face model downloads in the `model-cache` volume, and Piper voices in `piper-voices`. After the first AI deployment, download licence-approved Piper voices into the configured data directory:

```sh
docker compose -f docker-compose.yml -f docker-compose.prod.yml exec -T api \
  python -m piper.download_voices --data-dir /models/piper \
  en_US-lessac-medium hi_IN-pratham-medium
```

The deployment script verifies that the configured Ollama model is reachable before declaring a successful deployment. Text-to-speech loads independently of Whisper, so an audio playback request does not download or allocate the speech-to-text model.

## Acceptance gates

- `GET /api/v1/health/ready` is healthy.
- Register, create a workspace, and upload an actual PDF.
- Wait for `ready`; inspect worker logs on failure.
- Ask a page-location question and verify the citation opens the physical page.
- Test transcription and audio playback with selected voice/model licences cleared for the deployment.
