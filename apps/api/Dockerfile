FROM python:3.12-slim

WORKDIR /workspace/apps/api
ARG INSTALL_AI=false
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
RUN apt-get update && apt-get install -y --no-install-recommends tesseract-ocr libgomp1 && rm -rf /var/lib/apt/lists/*
# The Compose build context for this image is apps/api, so every source path
# below must be relative to that directory rather than the repository root.
COPY pyproject.toml ./
COPY app ./app
COPY migrations ./migrations
COPY alembic.ini ./alembic.ini
RUN pip install --no-cache-dir --retries 5 --timeout 120 . \
	&& if [ "$INSTALL_AI" = "true" ]; then pip install --no-cache-dir --retries 5 --timeout 120 ".[ai]"; fi
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
