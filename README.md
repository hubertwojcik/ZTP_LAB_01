# ZTP_LAB_01

FastAPI project with PostgreSQL database, Docker Compose, and Behave testing framework.

## Project Structure

```
.
├── src/                    # Application source code
│   ├── models/            # SQLAlchemy models
│   ├── main.py            # FastAPI application entry point
│   ├── config.py          # Configuration management
│   └── database.py        # Database connection and session management
├── features/              # Behave BDD tests
│   ├── environment.py     # Test environment setup
│   ├── steps/            # Step definitions
│   └── *.feature         # Feature files
├── alembic/              # Database migrations
├── docker-compose.yml    # PostgreSQL container configuration
├── requirements.txt      # Python dependencies
├── behave.ini            # Behave configuration
└── Makefile             # Useful commands

```

## Setup

### 1. Install dependencies

```bash
make install
# or
pip install -r requirements.txt
```

### 2. Start PostgreSQL with Docker

```bash
make dev-up
# or
docker-compose up -d
```

### 3. Copy environment variables

Create a Symfony file from the example:

```bash
cp .env.example .env
```

Edit `.env` if needed with your database credentials.

### 4. Run the application

```bash
make run
# or
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The application will be available at `http://localhost:8000`

## Available Commands

- `make install` - Install Python dependencies
- `make dev-up` - Start PostgreSQL in Docker
- `make dev-down` - Stop PostgreSQL in Docker
- `make run` - Run the FastAPI application
- `make test` - Run Behave tests
- `make clean` - Clean up generated files
- `make init-db` - Initialize database with Alembic migrations

## Database Migrations

To create and apply database migrations:

```bash
alembic revision --autogenerate -m "Your migration message"
alembic upgrade head
```

## Testing with Behave

Run BDD tests:

```bash
make test
# or
behave
```

## API Documentation

Once the application is running, access the interactive API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Configuration

All configuration is managed through `.env` file and `src/config.py` using Pydantic Settings.
