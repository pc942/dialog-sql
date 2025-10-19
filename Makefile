
SHELL := /bin/bash
.ONESHELL:

POETRY ?= poetry
COMPOSE := docker compose -f infra/docker/compose.yml

.PHONY: dev-up dev-down api-logs dbt-run dbt-docs fmt lint test

dev-up:
	$(COMPOSE) up -d --build

dev-down:
	$(COMPOSE) down

api-logs:
	$(COMPOSE) logs -f api

fmt:
	$(POETRY) run black .
	$(POETRY) run isort .

lint:
	$(POETRY) run flake8 services tests
	$(POETRY) run mypy services/api/app

test:
	$(POETRY) run pytest -q

dbt-run:
	cd analytics/dbt && $(POETRY) run dbt run

dbt-docs:
	cd analytics/dbt && $(POETRY) run dbt docs generate && $(POETRY) run dbt docs serve


eval:
	poetry run python scripts/evaluate_nl2sql.py --data evaluations/nl2sql.yaml

flight:
	docker compose -f infra/docker/compose.yml up -d flight
