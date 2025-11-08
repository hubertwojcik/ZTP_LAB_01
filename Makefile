.PHONY: help up down restart logs clean build test init

help:
	@echo "Available commands:"
	@echo "  make up       - Start all services (PostgreSQL + FastAPI)"
	@echo "  make down     - Stop all services"
	@echo "  make restart  - Restart all services"
	@echo "  make logs     - View logs from all services"
	@echo "  make build    - Rebuild Docker images"
	@echo "  make test     - Run integration tests (Behave)"
	@echo "  make clean    - Clean up generated files and volumes"
	@echo "  make init     - First-time setup (clean, build, up, migrate)"
	@echo ""
	@echo "Application will be available at: http://localhost:8000"
	@echo "Swagger docs at: http://localhost:8000/docs"
	@echo ""
	@echo "First time setup:"
	@echo "  1. make init"
	@echo "  2. make test"

up:
	docker-compose up -d
	@echo "✅ Services are starting up!"
	@echo "🌐 FastAPI will be available at http://localhost:8000"
	@echo "📚 Swagger docs at http://localhost:8000/docs"
	@echo "Use 'make logs' to see the logs"

down:
	docker-compose down

restart:
	docker-compose restart

logs:
	docker-compose logs -f

build:
	docker-compose build --no-cache

test:
	@echo "Running integration tests..."
	@docker-compose exec -T fastapi behave --no-capture --quiet --summary 2>&1 | tail -5 || python3 -m behave --no-capture --quiet --summary 2>&1 | tail -5

clean:
	docker-compose down -v
	find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -r {} + 2>/dev/null || true

init:
	@echo "🚀 First-time setup..."
	@echo "1. Cleaning up..."
	@docker-compose down -v 2>/dev/null || true
	@echo "2. Creating alembic/versions directory..."
	@mkdir -p alembic/versions
	@echo "3. Building Docker images..."
	@docker-compose build --no-cache
	@echo "4. Starting services..."
	@docker-compose up -d
	@echo "5. Waiting for services to be ready..."
	@sleep 5
	@echo "6. Creating database migration..."
	@docker-compose exec -T fastapi alembic revision --autogenerate -m "Initial migration" || true
	@echo "7. Applying migration..."
	@docker-compose exec -T fastapi alembic upgrade head
	@echo ""
	@echo "✅ Setup complete!"
	@echo "🌐 FastAPI: http://localhost:8000"
	@echo "📚 Swagger: http://localhost:8000/docs"
	@echo "🧪 Run tests: make test"
