import logging
import sys
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent.parent))

from app.scripts.init_db import init_db
from app.scripts.init_superuser import init_superuser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_all() -> None:
    try:
        # Initialize database tables
        logger.info("Initializing database tables...")
        init_db()
        
        # Initialize superuser
        logger.info("Initializing superuser...")
        init_superuser()
        
        logger.info("All initialization completed successfully")
    except Exception as e:
        logger.error(f"Error during initialization: {e}")
        raise

if __name__ == "__main__":
    init_all() 