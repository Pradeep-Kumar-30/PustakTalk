#!/usr/bin/env sh
set -eu
test -f .env || { echo '.env is required'; exit 1; }
compose() {
  docker compose -f docker-compose.yml -f docker-compose.prod.yml "$@"
}

compose up --build -d --wait --wait-timeout 180
compose exec -T api alembic upgrade head
if compose exec -T api python -c 'from app.core.config import get_settings; raise SystemExit(not get_settings().install_ai)'; then
  compose exec -T api python -c '
import json
from urllib.request import urlopen

from app.core.config import get_settings

settings = get_settings()
base_url = str(settings.ollama_base_url).rstrip("/")
with urlopen(f"{base_url}/api/tags", timeout=5) as response:
    installed_models = {item.get("name") for item in json.load(response).get("models", [])}
if settings.llm_model not in installed_models:
    raise SystemExit(f"Required Ollama model is unavailable: {settings.llm_model}")
'
fi
WEB_HEALTH_URL=http://localhost API_HEALTH_URL=http://localhost ./infrastructure/scripts/health-check.sh
