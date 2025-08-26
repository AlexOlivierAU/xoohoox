from datetime import timedelta
import logging
from typing import Any
from fastapi import APIRouter, Body, Depends, HTTPException, Form, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps
from app.core import security
from app.core.config import settings
from app.crud.user import user
from app.schemas.token import Token
from app.schemas.user import UserCreate, User, UserInDB

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/register", response_model=schemas.User)
def register(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
) -> Any:
    """
    Create new user.
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = crud.user.create(db, obj_in=user_in)
    return user

@router.post("/login/access-token", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user_obj = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif not crud.user.is_active(user_obj):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user_obj.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }

@router.post("/login/test-token", response_model=schemas.User)
def test_token(current_user: models.User = Depends(deps.get_current_user)) -> Any:
    """
    Test access token.
    """
    return current_user

@router.post("/refresh", response_model=schemas.Token)
def refresh_token(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
) -> Any:
    """
    Refresh access token.
    """
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            current_user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }

@router.post("/logout")
def logout(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
) -> Any:
    """
    Logout user and invalidate token.
    """
    # In a real implementation, you might want to:
    # 1. Add the token to a blacklist
    # 2. Clear any session data
    # 3. Update user's last logout time
    return {"message": "Successfully logged out"} 