.PHONY: help install dev-up dev-down test clean

help:
	@echo "Available commands:"
	@echo "  make install      - Install Python dependencies"
	@echo "  make dev-up       - Start PostgreSQL in Docker"
	@echo "  make dev-down     - Stop PostgreSQL in Docker"
	@echo "  make run          - Run the FastAPI application"
	@echo "  make test         - Run Behave tests"
	@echo "  make clean        - Clean up generated files"
	@echo "  make init-db      - Initialize database with Alembic"

install:
	pip install -r requirements.txt

dev-up:
	docker-compose up -d

dev-down:
	docker-compose down

run:
	uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

test:
	behave

clean:
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +

init-db:
	alembic revision --autogenerate -m "Initial migration"
	alembic upgrade head

