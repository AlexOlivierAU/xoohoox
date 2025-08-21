import logging
import sys
from typing import Any, Dict

from loguru import logger
from app.core.config import settings

class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )

def setup_logging() -> None:
    # Remove all existing handlers
    logging.root.handlers = []
    logging.root.setLevel(logging.INFO)

    # Add handlers for all loggers
    for name in logging.root.manager.loggerDict:
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    # Configure loguru
    logger.configure(
        handlers=[
            {
                "sink": sys.stdout,
                "level": logging.INFO,
                "format": "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            },
            {
                "sink": "logs/app.log",
                "level": logging.INFO,
                "rotation": "500 MB",
                "retention": "10 days",
                "format": "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
            },
            {
                "sink": "logs/error.log",
                "level": logging.ERROR,
                "rotation": "100 MB",
                "retention": "30 days",
                "format": "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
            },
            {
                "sink": "logs/maintenance.log",
                "level": logging.INFO,
                "rotation": "100 MB",
                "retention": "90 days",
                "format": "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
                "filter": lambda record: "maintenance" in record["name"].lower(),
            },
        ]
    )

    # Intercept standard logging
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

    # Set loguru as the default logger
    logging.getLogger().handlers = [InterceptHandler()]

def log_maintenance_event(
    event_type: str,
    maintenance_id: int,
    technician_id: int,
    details: Dict[str, Any],
) -> None:
    """
    Log a maintenance event with standardized format.
    
    Args:
        event_type: Type of maintenance event (e.g., 'create', 'update', 'delete')
        maintenance_id: ID of the maintenance record
        technician_id: ID of the technician performing the maintenance
        details: Additional details about the maintenance event
    """
    logger.bind(
        type="maintenance",
        event_type=event_type,
        maintenance_id=maintenance_id,
        technician_id=technician_id,
    ).info(
        f"Maintenance {event_type} | Maintenance ID: {maintenance_id} | Technician ID: {technician_id} | Details: {details}"
    ) 