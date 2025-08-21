import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from app.main import app
from app.core.config import settings

client = TestClient(app)

def test_login_success():
    """Test successful login."""
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD
    }
    
    response = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials():
    """Test login with invalid credentials."""
    login_data = {
        "username": "wrong@email.com",
        "password": "wrongpassword"
    }
    
    response = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data
    assert "Incorrect username or password" in data["detail"]

def test_login_empty_credentials():
    """Test login with empty credentials."""
    login_data = {
        "username": "",
        "password": ""
    }
    
    response = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    assert len(data["detail"]) > 0  # Should have validation errors

def test_get_current_user():
    """Test getting current user information."""
    # First login to get token
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD
    }
    
    login_response = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    
    # Then get current user
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get(f"{settings.API_V1_STR}/login/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "email" in data
    assert data["email"] == settings.FIRST_SUPERUSER
    assert "is_active" in data
    assert "is_superuser" in data

def test_get_current_user_invalid_token():
    """Test getting current user with invalid token."""
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get(f"{settings.API_V1_STR}/login/me", headers=headers)
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data
    assert "Could not validate credentials" in data["detail"]

def test_get_current_user_no_token():
    """Test getting current user without token."""
    response = client.get(f"{settings.API_V1_STR}/login/me")
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data
    assert "Not authenticated" in data["detail"]

def test_create_user():
    """Test user creation endpoint."""
    # First login as superuser
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD
    }
    
    login_response = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    
    # Create new user
    headers = {"Authorization": f"Bearer {token}"}
    user_data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "full_name": "Test User",
        "is_active": True,
        "is_superuser": False
    }
    
    response = client.post(
        f"{settings.API_V1_STR}/users/",
        headers=headers,
        json=user_data
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["full_name"] == user_data["full_name"]
    assert "id" in data

def test_create_user_unauthorized():
    """Test user creation without proper authorization."""
    user_data = {
        "email": "test2@example.com",
        "password": "testpassword123",
        "full_name": "Test User 2",
        "is_active": True,
        "is_superuser": False
    }
    
    response = client.post(f"{settings.API_V1_STR}/users/", json=user_data)
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data
    assert "Not authenticated" in data["detail"] 