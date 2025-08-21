from fastapi.testclient import TestClient
import pytest
from sqlalchemy.orm import Session

from app.main import app
from app.crud import user
from app.core.config import settings

def test_register_user(client: TestClient):
    # Test data
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpass123",
        "full_name": "Test User"
    }
    
    # Test registration
    response = client.post(
        f"{settings.API_V1_STR}/auth/register",
        json=user_data,
    )
    print(f"Response status: {response.status_code}")
    print(f"Response content: {response.content}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["username"] == user_data["username"]
    assert data["full_name"] == user_data["full_name"]
    assert "password" not in data
    
    # Test duplicate email
    response = client.post(
        f"{settings.API_V1_STR}/auth/register",
        json=user_data,
    )
    assert response.status_code == 400
    assert "email already exists" in response.json()["detail"]
    
    # Test duplicate username
    user_data["email"] = "another@example.com"
    response = client.post(
        f"{settings.API_V1_STR}/auth/register",
        json=user_data,
    )
    assert response.status_code == 400
    assert "username already exists" in response.json()["detail"]
    
    # Test invalid email
    user_data["email"] = "notanemail"
    response = client.post(
        f"{settings.API_V1_STR}/auth/register",
        json=user_data,
    )
    assert response.status_code == 422  # Validation error
    
    # Test missing required fields
    response = client.post(
        f"{settings.API_V1_STR}/auth/register",
        json={},
    )
    assert response.status_code == 422  # Validation error

def test_login(client: TestClient):
    # First register a user
    user_data = {
        "email": "login@example.com",
        "username": "loginuser",
        "password": "loginpass123",
        "full_name": "Login User"
    }
    
    client.post(
        f"{settings.API_V1_STR}/auth/register",
        json=user_data,
    )
    
    # Test successful login
    login_data = {
        "username": user_data["username"],
        "password": user_data["password"]
    }
    response = client.post(
        f"{settings.API_V1_STR}/auth/login/access-token",
        data=login_data,  # Note: using data instead of json for OAuth2 form data
    )
    assert response.status_code == 200
    tokens = response.json()
    assert "access_token" in tokens
    assert tokens["token_type"] == "bearer"
    
    # Test invalid password
    login_data["password"] = "wrongpass"
    response = client.post(
        f"{settings.API_V1_STR}/auth/login/access-token",
        data=login_data,
    )
    assert response.status_code == 400
    assert "Incorrect username or password" in response.json()["detail"]
    
    # Test non-existent user
    login_data["username"] = "nonexistent"
    response = client.post(
        f"{settings.API_V1_STR}/auth/login/access-token",
        data=login_data,
    )
    assert response.status_code == 400
    assert "Incorrect username or password" in response.json()["detail"] 