from typing import Dict, Optional
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.crud import user
from app.schemas.user import UserCreate
from app.core.config import settings

def create_random_user(
    client: TestClient,
    email: str = "test@example.com",
    password: str = "testpass123",
    username: str = "testuser",
    full_name: Optional[str] = None,
) -> Dict[str, str]:
    data = {
        "email": email,
        "password": password,
        "username": username,
        "full_name": full_name or "Test User"
    }
    response = client.post(
        f"{settings.API_V1_STR}/login/register",
        json=data,
    )
    return response.json()

def user_authentication_headers(
    client: TestClient, username: str, password: str
) -> Dict[str, str]:
    data = {"username": username, "password": password}
    response = client.post(
        f"{settings.API_V1_STR}/login/access-token", data=data
    )
    auth_token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers 