# ZTP_LAB_01

FastAPI project with PostgreSQL database, Docker Compose, and Behave testing framework.

## Quick Start 🚀

### Instalacja od zera (krok po kroku)

**1. Zatrzymaj i usuń wszystkie kontenery i wolumeny (jeśli istnieją):**

```bash
make clean
```

**2. Utwórz katalog na migracje (jeśli nie istnieje):**

```bash
mkdir -p alembic/versions
```

**3. Zbuduj obrazy Docker:**

```bash
make build
```

**4. Uruchom serwisy (PostgreSQL + FastAPI):**

```bash
make up
```

**5. Poczekaj kilka sekund, aż serwisy się uruchomią, a następnie zastosuj migracje bazy danych:**

```bash
docker-compose exec fastapi alembic revision --autogenerate -m "Initial migration"
docker-compose exec fastapi alembic upgrade head
```

**6. Sprawdź, czy wszystko działa:**

```bash
# Sprawdź status serwisów
docker-compose ps

# Uruchom testy
make test
```

**7. Sprawdź aplikację:**

- API: `http://localhost:8000`
- Swagger docs: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

### Szybki start (jeśli wszystko już jest skonfigurowane)

```bash
make up
```

The application will be available at `http://localhost:8000`  
Swagger docs: `http://localhost:8000/docs`

## Project Structure

```
.
├── src/                    # Application source code
│   ├── api/               # API endpoints
│   ├── models/            # SQLAlchemy models
│   ├── schemas/           # Pydantic schemas
│   ├── repositories/      # Data access layer
│   ├── services/          # Business logic layer
│   ├── main.py            # FastAPI application entry point
│   ├── config.py          # Configuration management
│   └── database.py        # Database connection and session management
├── features/              # Behave BDD tests
├── alembic/              # Database migrations
├── docker-compose.yml    # Docker Compose configuration
├── Dockerfile            # Python application container
├── requirements.txt      # Python dependencies
├── behave.ini            # Behave configuration
└── Makefile             # Useful commands
```

## Setup with Docker (Recommended)

### 1. Start all services

```bash
make up
```

This will:

- Start PostgreSQL database
- Build and start FastAPI application
- Wait for database to be ready
- Mount source code for hot-reload

### 2. View logs

```bash
make logs
```

### 3. Stop all services

```bash
make down
```

## Available Commands

| Command        | Description                               |
| -------------- | ----------------------------------------- |
| `make up`      | Start all services (PostgreSQL + FastAPI) |
| `make down`    | Stop all services                         |
| `make restart` | Restart all services                      |
| `make logs`    | View logs from all services               |
| `make build`   | Rebuild Docker images                     |
| `make clean`   | Clean up generated files and volumes      |

## Application Endpoints

Once running, the application provides:

- **Products**: `/api/v1/products` - Product management
- **Categories**: `/api/v1/categories` - Category management
- **Forbidden Phrases**: `/api/v1/forbidden-phrases` - Forbidden phrase management
- **Audit History**: `/api/v1/products/{id}/history` - Product change history
- **Swagger UI**: `/docs` - Interactive API documentation
- **ReDoc**: `/redoc` - Alternative API documentation

## Features

✅ **RESTful API** - Full CRUD operations  
✅ **Input Validation** - Pydantic schemas with detailed error messages  
✅ **Database Audit Trail** - Automatic tracking of product changes  
✅ **Forbidden Phrases** - Content moderation on product names  
✅ **Price Range Validation** - Category-based price constraints  
✅ **Swagger Documentation** - Auto-generated API docs  
✅ **Docker Support** - Complete containerization

## API Request/Response Examples

### Create a Category

```bash
POST /api/v1/categories
{
  "name": "Electronics",
  "description": "Electronic devices and accessories",
  "min_price": 10.0,
  "max_price": 5000.0
}
```

### Create a Product

```bash
POST /api/v1/products
{
  "name": "Laptop2024",
  "price": 1299.99,
  "quantity": 50,
  "category_id": 1
}
```

## Database Migrations

### Pierwsza instalacja

Przy pierwszej instalacji musisz utworzyć migracje:

```bash
# 1. Utwórz katalog na migracje (jeśli nie istnieje)
mkdir -p alembic/versions

# 2. Wygeneruj migrację na podstawie modeli
docker-compose exec fastapi alembic revision --autogenerate -m "Initial migration"

# 3. Zastosuj migrację
docker-compose exec fastapi alembic upgrade head
```

### Tworzenie nowych migracji

Gdy zmieniasz modele, utwórz nową migrację:

```bash
docker-compose exec fastapi alembic revision --autogenerate -m "Your migration message"
docker-compose exec fastapi alembic upgrade head
```

### Sprawdzanie statusu migracji

```bash
# Zobacz aktualną wersję
docker-compose exec fastapi alembic current

# Zobacz historię migracji
docker-compose exec fastapi alembic history
```

## Configuration

Environment variables are managed through:

- Docker Compose environment variables
- `.env` file (optional, for local development)

Default database credentials:

- User: `fastapi_user`
- Password: `fastapi_password`
- Database: `fastapi_db`
- Host: `postgres` (inside Docker network)

## Testing with Behave

The project includes comprehensive integration tests that verify all business requirements through HTTP API calls.

### Test Coverage

The test suite covers all business requirements:

✅ **Product Management**

- Creating products with validation
- Name validation (length, format, uniqueness, forbidden phrases)
- Price validation (positive, within category range)
- Quantity validation (non-negative)
- Category existence validation
- CRUD operations

✅ **Category Management**

- Creating categories with price constraints
- Name uniqueness validation
- Price range validation (max > min)

✅ **Forbidden Phrases**

- Creating and managing forbidden phrases
- Product name validation against forbidden phrases

✅ **Audit Trail**

- Automatic logging of product changes (CREATE, UPDATE, DELETE)
- History retrieval and validation

### Running Tests

Run all integration tests:

```bash
make test
```

Or run tests directly:

```bash
# Inside Docker container
docker-compose exec fastapi behave

# Or locally (if API is running)
python3 -m behave
```

### Test Structure

- `features/product_management.feature` - Product CRUD and validation tests
- `features/category_management.feature` - Category management tests
- `features/forbidden_phrases.feature` - Forbidden phrase tests
- `features/audit_trail.feature` - Audit trail verification tests
- `features/steps/` - Step definitions implementing HTTP API calls

All tests communicate with the API through HTTP requests using the `requests` library.

## Troubleshooting

### Application won't start

```bash
make logs  # Check logs for errors
make restart  # Try restarting
```

### Database connection issues

```bash
make down  # Stop everything
make up  # Start fresh
```

### Rebuild from scratch

```bash
make clean  # Remove volumes and cache
make build  # Rebuild images
make up  # Start services
```
