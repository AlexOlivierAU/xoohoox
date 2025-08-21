import logging
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from app.db.database import engine, Base
from app.core.logging import setup_logging
from app.core.config import settings
from app.api.v1.api import api_router

# Set up logging
loggers = setup_logging()
logger = logging.getLogger(__name__)

logger.debug("Starting application initialization")

try:
    # Create database tables
    logger.debug("Creating database tables")
    Base.metadata.create_all(bind=engine)
    logger.debug("Database tables created successfully")

    # Create FastAPI app
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )
    logger.debug("FastAPI app created")

    # Set up CORS middleware with hardcoded values
    origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,  # Use hardcoded origins instead of settings
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    logger.debug(f"CORS middleware configured with origins: {origins}")

    # Include API router
    app.include_router(api_router, prefix=settings.API_V1_STR)
    logger.debug("API router registered")

    # Request logging middleware
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time
        logger.info(
            f"Method: {request.method} Path: {request.url.path} "
            f"Status: {response.status_code} Duration: {duration:.2f}s"
        )
        return response

    # Error handlers
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.error(f"Validation error: {exc.errors()}")
        return JSONResponse(
            status_code=422,
            content={"detail": exc.errors()}
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        logger.error(f"HTTP error: {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled error: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )

    @app.get("/")
    def root():
        return {"message": f"Welcome to {settings.PROJECT_NAME}"}

    @app.get("/health")
    def health_check():
        return {"status": "ok"}

    @app.get("/api/v1/mock/batches")
    def mock_batches():
        """Mock batches endpoint for frontend testing"""
        return {
            "total": 12,
            "items": [
                {
                    "id": "1",
                    "batch_id": "XHR-20250413-01-01-B001",
                    "fruit_type": "Apple",
                    "process_type": "Juice",
                    "status": "active",
                    "start_date": "2024-04-13T10:00:00Z",
                    "expected_completion": "2024-04-20T10:00:00Z",
                    "current_stage": "fermentation",
                    "progress": 65.0,
                    "quantity": 100,
                    "unit": "L"
                },
                {
                    "id": "2", 
                    "batch_id": "XHR-20250413-01-02-B002",
                    "fruit_type": "Orange",
                    "process_type": "Juice",
                    "status": "completed",
                    "start_date": "2024-04-10T10:00:00Z",
                    "expected_completion": "2024-04-17T10:00:00Z",
                    "current_stage": "completed",
                    "progress": 100.0,
                    "quantity": 150,
                    "unit": "L"
                },
                {
                    "id": "3",
                    "batch_id": "XHR-20250413-01-03-B003", 
                    "fruit_type": "Lemon",
                    "process_type": "Juice",
                    "status": "in_progress",
                    "start_date": "2024-04-12T10:00:00Z",
                    "expected_completion": "2024-04-19T10:00:00Z",
                    "current_stage": "chemistry",
                    "progress": 25.0,
                    "quantity": 75,
                    "unit": "L"
                }
            ]
        }

    @app.get("/api/v1/mock/quality-checks")
    def mock_quality_checks():
        """Mock quality checks endpoint for frontend testing"""
        return {
            "total": 8,
            "items": [
                {
                    "id": "1",
                    "test_id": "QC-001",
                    "batch_id": "XHR-20250413-01-01-B001",
                    "test_type": "pH",
                    "result": "pass",
                    "test_date": "2024-04-13T14:00:00Z"
                },
                {
                    "id": "2",
                    "test_id": "QC-002", 
                    "batch_id": "XHR-20250413-01-01-B001",
                    "test_type": "Brix",
                    "result": "pass",
                    "test_date": "2024-04-13T15:00:00Z"
                },
                {
                    "id": "3",
                    "test_id": "QC-003",
                    "batch_id": "XHR-20250413-01-02-B002", 
                    "test_type": "pH",
                    "result": "pass",
                    "test_date": "2024-04-10T14:00:00Z"
                }
            ]
        }

    logger.debug("Application initialization completed")
except Exception as e:
    logger.error(f"Error during application startup: {str(e)}", exc_info=True)
    raise