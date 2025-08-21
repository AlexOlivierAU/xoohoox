from typing import Any, Dict, Optional, Union
import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

logger = logging.getLogger(__name__)

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        try:
            logger.info(f"Creating user with email: {obj_in.email}")
            db_obj = User(
                email=obj_in.email,
                hashed_password=get_password_hash(obj_in.password),
                full_name=obj_in.full_name,
                is_superuser=obj_in.is_superuser,
                is_active=obj_in.is_active
            )
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            logger.info(f"Successfully created user with ID: {db_obj.id}")
            return db_obj
        except SQLAlchemyError as e:
            logger.error(f"Database error during user creation: {str(e)}")
            db.rollback()
            raise
        except Exception as e:
            logger.error(f"Unexpected error during user creation: {str(e)}")
            db.rollback()
            raise

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data.get("password"):
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser

user = CRUDUser(User) 