#!/usr/bin/env sh
set -eu
test -f .env || cp .env.example .env
printf '%s\n' 'Ensure Ollama is running, then download the configured model with: ollama pull qwen3:0.6b'
docker compose up --build -d --wait --wait-timeout 180
