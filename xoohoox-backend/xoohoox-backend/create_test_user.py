from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.crud.user import user
from app.schemas.user import UserCreate

def create_test_user():
    db = SessionLocal()
    try:
        # Check if test user already exists
        if not user.get_by_email(db, email="test@example.com"):
            user_in = UserCreate(
                email="test@example.com",
                password="testpass123",
                full_name="Test User",
                is_superuser=True  # Making it a superuser for full access
            )
            user.create(db, obj_in=user_in)
            print("Test user created successfully!")
        else:
            print("Test user already exists!")
    finally:
        db.close()

if __name__ == "__main__":
    create_test_user() 