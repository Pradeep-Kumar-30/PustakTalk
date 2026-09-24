#!/usr/bin/env sh
set -eu
docker compose exec -T api alembic upgrade head
