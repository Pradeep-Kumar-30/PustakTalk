FROM python:3.12-slim

WORKDIR /workspace
ARG INSTALL_AI=false
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
RUN apt-get update && apt-get install -y --no-install-recommends tesseract-ocr libgomp1 && rm -rf /var/lib/apt/lists/*
COPY apps/api ./apps/api
COPY workers/document-worker ./workers/document-worker
RUN pip install --no-cache-dir --retries 5 --timeout 120 ./apps/api ./workers/document-worker \
	&& if [ "$INSTALL_AI" = "true" ]; then pip install --no-cache-dir --retries 5 --timeout 120 "./apps/api[ai]"; fi
CMD ["arq", "worker.main.WorkerSettings"]
