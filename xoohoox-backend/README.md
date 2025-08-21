# Xoohoox Backend

A modern, scalable backend for fermentation and distillation management, built with FastAPI and SQLAlchemy 2.0.

## Features

- **Batch Management**
  - Track production batches with detailed status tracking
  - Monitor fermentation and distillation stages
  - Record quality metrics and processing parameters
  - Support for multiple fruit types and juice processing methods

- **Equipment Management**
  - Comprehensive equipment tracking and maintenance scheduling
  - Status monitoring (operational, maintenance, repair, etc.)
  - Maintenance history and scheduling
  - Equipment type categorization

- **Quality Control**
  - Chemical analysis tracking
  - Physical property monitoring
  - Sensory evaluation support
  - Microbiological testing
  - Environmental impact assessment

- **Inventory Management**
  - Raw material tracking
  - Finished product inventory
  - Packaging materials management
  - Chemical inventory control
  - Supply chain monitoring

## Development

### Backend Stack
- Python 3.11+
- FastAPI for high-performance API
- SQLAlchemy 2.0 for modern ORM
- Pydantic v2 for data validation
- Alembic for database migrations
- pytest for testing

### Database
- SQLite for development
- PostgreSQL for production
- Support for multiple database backends

### Testing
- Comprehensive test suite
- CRUD operation testing
- Model validation testing
- Status transition testing
- Equipment maintenance testing

## Models

### Batch
- Tracks production batches
- Manages fermentation and distillation stages
- Records quality metrics
- Supports multiple fruit types
- Handles juice processing methods

### Equipment
- Equipment type categorization
- Status tracking
- Maintenance scheduling
- Performance monitoring
- Usage history

### Maintenance
- Preventive maintenance
- Corrective maintenance
- Calibration tracking
- Inspection records
- Cleaning schedules

## Getting Started

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up the database:
   ```bash
   alembic upgrade head
   ```
5. Run the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

## Testing

Run the test suite:
```bash
python -m pytest tests/ -v
```

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 