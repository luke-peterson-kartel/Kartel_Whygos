"""
FastAPI Configuration using Pydantic Settings
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # App settings
    app_name: str = "Kartel WhyGO Management API"
    version: str = "1.0.0"
    debug: bool = True

    # Security settings
    secret_key: str  # REQUIRED - must be set in .env
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 10080  # 1 week default

    # CORS settings
    allowed_origins: List[str] = ["http://localhost:3000"]

    # Data paths
    data_dir: str = "data"

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
