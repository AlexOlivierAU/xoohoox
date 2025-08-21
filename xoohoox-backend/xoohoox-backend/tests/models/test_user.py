import pytest
from datetime import datetime
from app.models.user import User

def test_user_creation():
    """Test creating a user with valid data."""
    user = User(
        email="test@example.com",
        hashed_password="hashedpass123",
        full_name="Test User",
        is_active=True,
        is_superuser=False
    )
    
    assert user.email == "test@example.com"
    assert user.hashed_password == "hashedpass123"
    assert user.full_name == "Test User"
    assert user.is_active is True
    assert user.is_superuser is False

def test_user_defaults():
    """Test default values for user fields."""
    user = User(
        email="test@example.com",
        hashed_password="hashedpass123"
    )
    
    assert user.is_active is True  # Should default to True
    assert user.is_superuser is False  # Should default to False
    assert user.full_name is None  # Should default to None

def test_user_representation():
    """Test string representation of User model."""
    user = User(
        email="test@example.com",
        hashed_password="hashedpass123",
        full_name="Test User"
    )
    
    str_repr = str(user)
    assert "User" in str_repr
    assert "test@example.com" in str_repr

def test_user_to_dict():
    """Test the to_dict method of User model."""
    user = User(
        email="test@example.com",
        hashed_password="hashedpass123",
        full_name="Test User",
        is_active=True,
        is_superuser=False
    )
    
    user_dict = user.to_dict()
    
    assert user_dict['email'] == "test@example.com"
    assert 'hashed_password' not in user_dict  # Password should not be included
    assert user_dict['full_name'] == "Test User"
    assert user_dict['is_active'] is True
    assert user_dict['is_superuser'] is False
    assert 'created_at' in user_dict
    assert 'updated_at' in user_dict

def test_user_timestamps():
    """Test that user model includes timestamps."""
    user = User(
        email="test@example.com",
        hashed_password="hashedpass123"
    )
    
    assert hasattr(user, 'created_at')
    assert hasattr(user, 'updated_at')
    assert isinstance(user.created_at, datetime)
    assert isinstance(user.updated_at, datetime)

def test_user_email_required():
    """Test that email is required for User model."""
    with pytest.raises(TypeError):
        User(hashed_password="hashedpass123")

def test_user_hashed_password_required():
    """Test that hashed_password is required for User model."""
    with pytest.raises(TypeError):
        User(email="test@example.com") 