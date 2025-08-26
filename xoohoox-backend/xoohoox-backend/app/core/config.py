from typing import List
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, field_validator

class Settings(BaseSettings):
    PROJECT_NAME: str = "Xoohoox Distillation Management System"
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ]
    ENVIRONMENT: str = "development"

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str]:
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v

    # Database
    SQLALCHEMY_DATABASE_URI: str = "postgresql://xoohoox:xoohoox123@localhost:5432/xoohoox"
    TEST_DATABASE_URI: str = "postgresql://xoohoox:xoohoox123@localhost:5432/xoohoox_test"

    # Security
    SECRET_KEY: str = "your-secret-key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    ALGORITHM: str = "HS256"

    class Config:
        case_sensitive = True

settings = Settings() 