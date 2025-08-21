import logging
import sys
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent.parent))

from app.scripts.init_db import init_db
from app.scripts.init_superuser import init_superuser

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main() -> None:
    logger.info("Starting initialization process...")
    try:
        # Initialize database
        logger.info("Initializing database...")
        init_db()
        
        # Initialize superuser
        logger.info("Initializing superuser...")
        init_superuser()
        
        logger.info("Initialization completed successfully!")
        
    except Exception as e:
        logger.error(f"Initialization failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 