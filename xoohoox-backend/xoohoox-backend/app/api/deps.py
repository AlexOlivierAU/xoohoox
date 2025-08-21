from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.core import security
from app.core.config import settings
from app.db.database import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db() -> Generator:
    """
    Get database session.
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    """
    Get current user from token.
    """
    # For now, just return a dummy user
    return "testuser"

def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def get_current_active_superuser(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user 