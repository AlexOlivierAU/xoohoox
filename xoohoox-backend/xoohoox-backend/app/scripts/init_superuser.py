import logging
import sys
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent.parent))

from app.core.config import settings
from app.core.security import get_password_hash
from app.db.session import SessionLocal
from app.models.user import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_superuser() -> None:
    db = SessionLocal()
    try:
        # Check if superuser already exists
        superuser = db.query(User).filter(User.email == settings.FIRST_SUPERUSER).first()
        if superuser:
            logger.info("Superuser already exists")
            return

        # Create superuser
        superuser = User(
            email=settings.FIRST_SUPERUSER,
            username=settings.FIRST_SUPERUSER.split('@')[0],  # Use part before @ as username
            hashed_password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
            full_name="Super Admin",
            is_superuser=True,
            is_active=True,
        )
        db.add(superuser)
        db.commit()
        logger.info("Superuser created successfully")
        
    except Exception as e:
        logger.error(f"Error creating superuser: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_superuser() 