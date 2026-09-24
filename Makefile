.DEFAULT_GOAL := help

PYTHON ?= .venv/bin/python
PIP = $(PYTHON) -m pip

.PHONY: help setup up down logs dev migrate test lint eval build deploy

help:
	@printf "PustakTalk targets: setup, up, down, logs, dev, migrate, test, lint, eval, build, deploy\n"

setup:
	python3 -m venv .venv
	$(PIP) install --upgrade pip
	$(PIP) install -e "apps/api[dev]"
	$(PIP) install -e workers/document-worker
	npm --prefix apps/web ci

up:
	docker compose up --build -d --wait --wait-timeout 180

down:
	docker compose down

logs:
	docker compose logs -f

dev:
	$(MAKE) up

migrate:
	docker compose exec -T api alembic upgrade head

test:
	PYTHONPATH=apps/api:workers/document-worker $(PYTHON) -m pytest apps/api/tests workers/document-worker/tests
	npm --prefix apps/web test -- --run

lint:
	$(PYTHON) -m ruff check apps/api workers/document-worker evaluation
	npm --prefix apps/web run lint

eval:
	PYTHONPATH=apps/api $(PYTHON) -m evaluation.runners.run_evaluation

build:
	docker compose build

deploy:
	./infrastructure/scripts/deploy.sh
