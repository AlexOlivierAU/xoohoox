import logging
import logging.handlers
import os
from app.core.config import settings

def setup_logging():
    """Configure application-wide logging with file rotation and different formatters."""
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_formatter = logging.Formatter(
        '%(levelname)s: %(message)s'
    )

    # File handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        f"{log_dir}/app.log",
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(file_formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)

    # Root logger configuration
    root_logger = logging.getLogger()
    root_logger.setLevel(
        logging.DEBUG if settings.ENVIRONMENT == "development"
        else logging.INFO
    )
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    # Create loggers for different components
    loggers = {
        'api': logging.getLogger('api'),
        'database': logging.getLogger('database'),
        'security': logging.getLogger('security'),
        'batch': logging.getLogger('batch'),
        'quality': logging.getLogger('quality'),
        'equipment': logging.getLogger('equipment')
    }

    # Configure component loggers
    for logger in loggers.values():
        logger.setLevel(root_logger.level)
        logger.propagate = True

    return loggers 