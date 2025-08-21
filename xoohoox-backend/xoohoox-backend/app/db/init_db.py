from sqlalchemy.orm import Session
from app.db.base import Base
from app.db.session import engine
from app.core.config import settings
from app.crud.user import user
from app.schemas.user import UserCreate
from app.db.test_data import create_test_batches

def init_db(db: Session) -> None:
    Base.metadata.create_all(bind=engine)
    
    # Create initial superuser if it doesn't exist
    user_obj = user.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if not user_obj:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            username=settings.FIRST_SUPERUSER,
            is_superuser=True,
            full_name="Initial Superuser",
        )
        user.create(db, obj_in=user_in)
    
    # Create test data
    create_test_batches(db) 