# Nelavista monorepo — root task runner.
# `make help` lists everything. V1 targets are prefixed v1- and never touch V2.
.DEFAULT_GOAL := help
SHELL := /bin/bash

help: ## Show this help
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-22s\033[0m %s\n", $$1, $$2}'

# ---------------------------------------------------------------- setup / infra
bootstrap: ## Install JS + Python deps and git hooks (<15 min, web + API)
	pnpm install
	uv sync --all-packages || pip install -e apps/api
	pre-commit install || echo "pre-commit not installed; run: pip install pre-commit"
	@echo "Bootstrap done. Next: make up && make seed-local; then make api-dev and make worker-dev (two terminals) and make dev (a third)."

up: ## Start local services (Postgres+pgvector, Redis, Mailpit)
	docker compose up -d

down: ## Stop local services
	docker compose down

reset-db: ## DESTROY local DB volume and recreate (local only)
	docker compose down -v && docker compose up -d db

seed-local: ## Seed fake sample data (prod-guarded; never touches real data)
	uv run --package nelavista-api python -m tools.seed_local

# ---------------------------------------------------------------- run
dev: ## Run web + admin together (start the API with `make api-dev` first)
	pnpm dev

api-dev: ## Run the API only (http://localhost:8000)
	uv run --package nelavista-api uvicorn app.main:app --reload --port 8000 --app-dir apps/api

worker-dev: ## Run the background worker only (sends queued email)
	uv run --package nelavista-api python -m app.worker

web-dev: ## Run the web app only (http://localhost:5173)
	pnpm --filter @nelavista/web dev

admin-dev: ## Run the admin app only (http://localhost:5174)
	pnpm --filter @nelavista/admin dev

mobile-start: ## Start the Expo dev server
	pnpm --filter @nelavista/mobile start

mobile-android: ## Open the app in the Android Emulator
	pnpm --filter @nelavista/mobile android

# ---------------------------------------------------------------- quality
lint: ## Lint everything (ruff + eslint)
	uv run ruff check . || ruff check .
	pnpm lint

typecheck: ## Typecheck everything
	pnpm typecheck

format: ## Format (prettier + ruff)
	pnpm format
	uv run ruff format . || ruff format .

test: ## Run V2 API tests
	cd apps/api && python -m pytest -q

test-v1: ## Run V1 tests (never run migrations/seed alongside this)
	python -m pytest tests/

load-test: ## Read-path p95 vs the 300 ms budget (F6; needs a running API + account)
	python tools/load_read_paths.py --base-url $(or $(BASE_URL),http://localhost:8000) \
		--email "$(EMAIL)" --password "$(PASSWORD)"

db-upgrade: ## Apply V2 API migrations (names its target first)
	uv run --package nelavista-api alembic -c apps/api/alembic.ini upgrade head

db-heads: ## Show V2 API migration heads (must be exactly one)
	uv run --package nelavista-api alembic -c apps/api/alembic.ini heads

api-client: ## Regenerate the typed API client
	pnpm generate:api-client

.PHONY: help bootstrap up down reset-db seed-local dev api-dev worker-dev web-dev admin-dev mobile-start mobile-android lint typecheck format test test-v1 load-test db-upgrade db-heads api-client
