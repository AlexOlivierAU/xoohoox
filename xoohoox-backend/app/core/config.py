from typing import List
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, field_validator

class Settings(BaseSettings):
    PROJECT_NAME: str = "Xoohoox Distillation Management System"
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    ENVIRONMENT: str = "development"

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Database
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./test.db"
    TEST_DATABASE_URI: str = "sqlite:///./test.db"

    # Security
    SECRET_KEY: str = "your-secret-key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    ALGORITHM: str = "HS256"

    class Config:
        case_sensitive = True

settings = Settings() 