.PHONY: help build up down logs test lint ingest

help:
	@echo "Commands:"
	@echo "  build    : Build docker images"
	@echo "  up       : Start services with docker-compose"
	@echo "  down     : Stop services"
	@echo "  logs     : Tail logs from services"
	@echo "  test     : Run tests"
	@echo "  lint     : Lint the codebase"
	@echo "  ingest   : Run the data ingestion process"

build:
	@docker-compose build

up:
	@docker-compose up -d

down:
	@docker-compose down

logs:
	@docker-compose logs -f

test:
	@docker-compose run --rm backend pytest

lint:
	@docker-compose run --rm backend flake8 app
	@docker-compose run --rm backend black app --check
	@docker-compose run --rm backend isort app --check-only

ingest:
	@docker-compose run --rm etl python etl/ingest_argovis.py
