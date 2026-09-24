#!/usr/bin/env sh
set -eu
web_url=${WEB_HEALTH_URL:-http://localhost:3000}
api_url=${API_HEALTH_URL:-http://localhost:8000}

curl --fail --silent --show-error "${api_url%/}/api/v1/health/ready"
curl --fail --silent --show-error "${web_url%/}/"
