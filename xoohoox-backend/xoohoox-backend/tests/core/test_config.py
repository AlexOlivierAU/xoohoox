import os
import pytest
from unittest.mock import patch
from app.core.config import Settings

def test_settings_load():
    """Test that settings load correctly."""
    settings = Settings()
    assert settings.PROJECT_NAME == "Xoohoox Juice Production Management"
    assert settings.API_V1_STR == "/api/v1"
    assert len(settings.SECRET_KEY) > 0
    assert settings.ACCESS_TOKEN_EXPIRE_MINUTES == 480
    assert settings.ALGORITHM == "HS256"

def test_database_uri_default():
    """Test database URI construction in default environment."""
    settings = Settings()
    assert settings.database_uri == "postgresql://postgres:postgres@localhost:5432/xoohoox"

def test_database_uri_testing():
    """Test database URI switches to SQLite in testing environment."""
    # Save current environment
    current_env = os.environ.get("ENVIRONMENT")
    
    try:
        # Set testing environment
        os.environ["ENVIRONMENT"] = "testing"
        settings = Settings()
        assert settings.database_uri == "sqlite:///./test.db"
    finally:
        # Restore environment
        if current_env:
            os.environ["ENVIRONMENT"] = current_env
        else:
            del os.environ["ENVIRONMENT"]

def test_cors_origins():
    """Test CORS origins configuration."""
    settings = Settings()
    expected_origins = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost:8001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
        "http://127.0.0.1:8001"
    ]
    assert settings.BACKEND_CORS_ORIGINS == expected_origins

def test_settings_environment_variables():
    """Test that settings can be overridden by environment variables."""
    # Set environment variables
    env_vars = {
        "API_V1_STR": "/api/v2",
        "ACCESS_TOKEN_EXPIRE_MINUTES": "60",
        "ALGORITHM": "HS512",
        "DATABASE_URL": "postgresql://user:pass@localhost:5432/testdb",
        "REDIS_URL": "redis://localhost:6379/1",
        "ENVIRONMENT": "production",
        "PROJECT_NAME": "Test Project",
        "FIRST_SUPERUSER": "test@example.com",
        "FIRST_SUPERUSER_PASSWORD": "testpass"
    }
    
    with patch.dict(os.environ, env_vars, clear=True):
        test_settings = Settings()
        
        # Check that environment variables override defaults
        assert test_settings.API_V1_STR == "/api/v2"
        assert test_settings.ACCESS_TOKEN_EXPIRE_MINUTES == 60
        assert test_settings.ALGORITHM == "HS512"
        assert test_settings.DATABASE_URL == "postgresql://user:pass@localhost:5432/testdb"
        assert test_settings.database_uri == "postgresql://user:pass@localhost:5432/testdb"

def test_settings_case_sensitive():
    """Test that settings are case sensitive."""
    # Create a new Settings instance
    test_settings = Settings()
    
    # Check that settings are case sensitive
    assert test_settings.API_V1_STR == "/api/v1"
    with pytest.raises(AttributeError):
        _ = test_settings.api_v1_str  # This should not exist

def test_settings_singleton():
    """Test that settings is a singleton instance."""
    # Get the global settings instance
    from app.core.config import settings as global_settings
    
    # Create a new instance
    new_settings = Settings()
    
    # They should be the same instance
    assert global_settings is new_settings