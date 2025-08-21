import pytest
from datetime import datetime, timedelta
from jose import jwt
from app.core.security import (
    create_access_token,
    verify_password,
    get_password_hash,
    settings
)

def test_create_access_token_default_expiry():
    """Test that create_access_token creates a token with the default expiry time."""
    # Create a token with default expiry
    subject = "test@example.com"
    token = create_access_token(subject)
    
    # Decode the token
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    
    # Check the token payload
    assert payload["sub"] == subject
    assert "exp" in payload
    
    # Check that the expiry is set to the default value
    exp = datetime.fromtimestamp(payload["exp"])
    now = datetime.utcnow()
    expected_exp = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Allow for a small time difference (1 second)
    assert abs((exp - expected_exp).total_seconds()) < 1

def test_create_access_token_custom_expiry():
    """Test that create_access_token creates a token with a custom expiry time."""
    # Create a token with custom expiry
    subject = "test@example.com"
    expires_delta = timedelta(minutes=30)
    token = create_access_token(subject, expires_delta=expires_delta)
    
    # Decode the token
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    
    # Check the token payload
    assert payload["sub"] == subject
    assert "exp" in payload
    
    # Check that the expiry is set to the custom value
    exp = datetime.fromtimestamp(payload["exp"])
    now = datetime.utcnow()
    expected_exp = now + expires_delta
    
    # Allow for a small time difference (1 second)
    assert abs((exp - expected_exp).total_seconds()) < 1

def test_verify_password():
    """Test that verify_password correctly verifies passwords."""
    # Create a hashed password
    password = "testpassword123"
    hashed_password = get_password_hash(password)
    
    # Verify the password
    assert verify_password(password, hashed_password) is True
    
    # Verify with incorrect password
    assert verify_password("wrongpassword", hashed_password) is False

def test_get_password_hash():
    """Test that get_password_hash creates different hashes for different passwords."""
    # Create hashed passwords
    password1 = "testpassword123"
    password2 = "testpassword456"
    
    hashed_password1 = get_password_hash(password1)
    hashed_password2 = get_password_hash(password2)
    
    # Check that the hashes are different
    assert hashed_password1 != hashed_password2
    
    # Check that the hashes are not the same as the original passwords
    assert hashed_password1 != password1
    assert hashed_password2 != password2
    
    # Check that the hashes start with the bcrypt identifier
    assert hashed_password1.startswith("$2b$")
    assert hashed_password2.startswith("$2b$") 