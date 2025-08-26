# Xoohoox Backend

## Overview
Xoohoox is a distillation management system backend that provides API endpoints for managing batches, quality control, and production processes.

## Tech Stack
- Python 3.9+
- FastAPI
- SQLAlchemy
- Pydantic
- PostgreSQL
- Alembic (for migrations)

## Project Structure
```
app/
├── api/                # API endpoints
│   └── v1/             # API version 1
│       └── endpoints/  # API route handlers
├── core/               # Core functionality
│   ├── config.py       # Configuration settings
│   └── security.py     # Security utilities
├── db/                 # Database
│   ├── base.py         # Base models
│   └── session.py      # Database session
├── models/             # SQLAlchemy models
├── schemas/            # Pydantic schemas
└── services/           # Business logic
```

## API Endpoints
The API provides the following main endpoints:

- `/api/v1/batches`: Batch management
- `/api/v1/quality`: Quality control
- `/api/v1/maintenance`: Equipment maintenance
- `/api/v1/users`: User management
- `/api/v1/auth`: Authentication

## Data Models
The system includes the following main models:

- **Batch**: Represents a distillation batch
- **QualityTest**: Quality control tests for batches
- **MaintenanceLog**: Equipment maintenance records
- **User**: System users with role-based access

## Getting Started

### Prerequisites
- Python 3.9+
- PostgreSQL
- Virtual environment (recommended)

### Installation
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run migrations
alembic upgrade head

# Start the server
uvicorn app.main:app --reload
```

## Development Guidelines
- Follow FastAPI best practices
- Use type hints throughout the codebase
- Write tests for all new features
- Document API endpoints using FastAPI's built-in documentation

## Testing
```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=app
```

## Features

- **Batch Management API**: Create, read, update, and delete batches
- **Quality Control API**: Record and retrieve quality measurements
- **Equipment Management API**: Track equipment status and maintenance
- **Real-time Updates**: WebSocket integration for live data
- **Authentication**: JWT-based authentication
- **Database**: SQLAlchemy ORM with PostgreSQL
- **Migrations**: Alembic for database migrations
- **Testing**: Pytest for unit and integration tests
- **Logging**: Comprehensive logging system
- **Documentation**: OpenAPI/Swagger documentation

## Prerequisites

- Python 3.11+
- PostgreSQL 14+
- Redis 6+ (for WebSocket support)
- pip (Python package manager)
- virtualenv (optional, but recommended)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-org/xoohoox-backend.git
   cd xoohoox-backend
   ```

2. Run the setup script:
   ```bash
   ./scripts/setup_dev.sh
   ```

   This script will:
   - Create a virtual environment
   - Install dependencies
   - Create necessary directories
   - Copy the development environment file
   - Run database migrations
   - Create a test user
   - Run tests

3. Start the development server:
   ```bash
   ./dev.sh
   ```

## Development

### Project Structure

```
xoohoox-backend/
├── alembic/                  # Database migrations
├── app/                      # Application code
│   ├── api/                  # API endpoints
│   │   └── v1/               # API version 1
│   │       ├── endpoints/    # API route handlers
│   │       └── deps.py       # Dependency injection
│   │   └── v1/               # API version 1
│   │       └── endpoints/    # API route handlers
│   ├── core/                 # Core functionality
│   │   ├── config.py         # Configuration
│   │   ├── security.py       # Security utilities
│   │   └── events.py         # Event handlers
│   ├── db/                   # Database
│   │   ├── base.py           # Base model
│   │   └── session.py        # Database session
│   ├── models/               # SQLAlchemy models
│   ├── schemas/              # Pydantic schemas
│   └── services/             # Business logic
├── logs/                     # Application logs
├── tests/                    # Test suite
├── scripts/                  # Utility scripts
├── .env                      # Environment variables
├── .env.development          # Development environment variables
├── alembic.ini               # Alembic configuration
├── dev.sh                    # Development server script
├── requirements.txt          # Python dependencies
├── run_dev.py                # Development server
└── setup_dev.sh              # Setup script
```

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/xoohoox

# Security
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# WebSocket
REDIS_URL=redis://localhost:6379/0

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# API
API_V1_STR=/api/v1
PROJECT_NAME=Xoohoox
BACKEND_CORS_ORIGINS=["http://localhost:3000"]
```

### API Documentation

Once the server is running, you can access the API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Available Scripts

- `./dev.sh`: Start the development server
- `./scripts/setup_dev.sh`: Set up the development environment
- `./scripts/create_test_user.py`: Create a test user
- `pytest`: Run tests
- `alembic upgrade head`: Run database migrations
- `alembic revision --autogenerate -m "description"`: Generate a new migration

### Testing

The project uses pytest for testing. The test suite is organized into several categories:

### Test Structure

```
tests/
├── core/               # Core functionality tests
│   ├── test_config.py  # Configuration and settings tests
│   └── test_security.py # Security and authentication tests
├── crud/               # CRUD operation tests
│   ├── test_crud.py    # Base CRUD test class
│   ├── test_user.py    # User model CRUD tests
│   ├── test_batch.py   # Batch model CRUD tests
│   ├── test_equipment.py # Equipment model CRUD tests
│   └── test_maintenance.py # Maintenance model CRUD tests
├── schemas/            # Schema validation tests
│   ├── test_batch_schemas.py  # Batch schema tests
│   └── test_user_schemas.py   # User schema tests
└── features/           # Feature-specific tests
    └── test_production_features.py  # Production process tests
```

### Test Categories

1. **Core Tests**
   - Configuration management
   - Environment settings
   - Security features
   - Authentication

2. **CRUD Tests**
   - Base CRUD operations
   - Model-specific operations
   - Error handling
   - Edge cases

3. **Schema Tests**
   - Data validation
   - Serialization/deserialization
   - Custom validators
   - Business rules

4. **Feature Tests**
   - Chemistry adjustment tracking
   - Fermentation kinetics monitoring
   - Distillation ladder progression
   - Trial management
   - Environmental impact tracking

### Running Tests

```bash
# Run all tests
pytest

# Run specific test category
pytest tests/core/
pytest tests/crud/
pytest tests/schemas/
pytest tests/features/

# Run with coverage report
pytest --cov=app tests/

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/core/test_config.py
```

### Test Coverage

The test suite covers:
- All CRUD operations for each model
- Data validation and business rules
- Process monitoring and tracking
- Environmental impact measurement
- Quality control procedures
- Equipment maintenance
- User authentication and authorization

## Deployment

### Production Setup

1. Set up a production environment with:
   - PostgreSQL database
   - Redis for WebSocket support
   - Nginx as a reverse proxy
   - Gunicorn as the WSGI server

2. Create a production environment file:
   ```bash
   cp .env.example .env.production
   # Edit .env.production with production values
   ```

3. Build and run with Docker:
   ```bash
   docker-compose up -d
   ```

### Docker Deployment

The project includes a Dockerfile and docker-compose.yml for containerized deployment:

```bash
# Build the Docker image
docker build -t xoohoox-backend .

# Run with docker-compose
docker-compose up -d
```

## WebSocket Integration

The backend provides WebSocket endpoints for real-time updates:

- Connect to `ws://localhost:8000/ws` (development) or `wss://api.xoohoox.com/ws` (production)
- Authenticate using the JWT token
- Subscribe to events for batches, equipment, and quality measurements
- Receive real-time updates when data changes

See the [API Integration Guide](API_INTEGRATION.md) for detailed WebSocket documentation.

## License

This project is licensed under the ISC License. 

## 🧩 XooHooX Dev Pack Integration

This repo is backed by a complete UI-to-backend mapping reference.

If you're working with the Uizard prototype or aligning frontend screens to backend models, see:

- `README_for_cursor.md` – API and data model mapping from screen flow
- `schemas/` – JSON schema definitions (batches, evaluations, yeasts)
- `models/` – Python Pydantic models
- `openapi.yaml` – Complete OpenAPI spec