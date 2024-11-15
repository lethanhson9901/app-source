from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # Application Settings
    APP_NAME: str = "Python Application"
    APP_VERSION: str = "1.0.0"
    API_KEY: str = "your-secret-api-key"  # Default for development
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    
    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8080
    
    # CORS Settings
    ALLOWED_ORIGINS: List[str] = ["*"]
    
    # Database Settings
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/db"
    
    # Redis Settings
    REDIS_URL: str = "redis://localhost:6379"
    
    # Metrics
    ENABLE_METRICS: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = True
        env_prefix = ""

settings = Settings()