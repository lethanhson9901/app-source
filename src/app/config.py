import json
import logging
import os
from pathlib import Path
from typing import Any, cast

from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)


def find_env_file() -> str:
    """
    Find the .env file by walking up the directory tree.

    Returns:
        str: Path to the found .env file or '.env' as fallback
    """
    current_dir = Path.cwd()
    while current_dir != current_dir.parent:
        env_file = current_dir / ".env"
        if env_file.exists():
            return str(env_file)
        current_dir = current_dir.parent
    return ".env"  # fallback to default


def get_default_host() -> str:
    """
    Determine the default host based on environment.

    For container/production use, override with APP_HOST environment variable.
    Returns localhost by default for security.

    Returns:
        str: The appropriate host binding
    """
    # Allow explicit override through environment variable
    if host := os.getenv("APP_HOST"):
        return host

    # Default to localhost for maximum security
    return "127.0.0.1"


class Settings(BaseSettings):
    # Docker Registry Settings
    GITHUB_USERNAME: str = "lethanhson9901"
    IMAGE_NAME: str = "app-source"
    BRANCH: str = "main"
    BUILD_VERSION: str = "1.0.0"

    # Removed duplicate DOCKER_REGISTRY definition

    #######################################
    # Core Application Settings
    #######################################
    APP_NAME: str = "Python Application"
    APP_VERSION: str = "1.0.0"
    APP_ENVIRONMENT: str = "development"
    APP_DEBUG: bool = False
    APP_HOST: str = get_default_host()
    APP_PORT: int = 8080
    APP_LOG_LEVEL: str = "INFO"

    # API Security
    API_KEY: str = "dev-secret-key"
    API_RATE_LIMIT: str = "100/minute"
    API_TIMEOUT: int = 30

    #######################################
    # Database Configuration
    #######################################
    DB_USER: str = "user"
    DB_PASSWORD: str = "password"
    DB_NAME: str = "db"
    DB_HOST: str = "postgres"
    DB_PORT: int = 5432
    DB_SSL_MODE: str = "disable"
    DB_MAX_CONNECTIONS: int = 100
    DB_IDLE_TIMEOUT: int = 300
    DB_CONNECT_TIMEOUT: int = 10
    DATABASE_URL: str | None = None

    #######################################
    # Redis Configuration
    #######################################
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = "redis"
    REDIS_DB: int = 0
    REDIS_SSL: bool = False
    REDIS_TIMEOUT: int = 5
    REDIS_URL: str | None = None

    #######################################
    # Security Configuration
    #######################################
    CORS_ALLOWED_ORIGINS: list[str] = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_MAX_AGE: int = 3600

    SECURITY_HSTS_ENABLED: bool = True
    SECURITY_HSTS_MAX_AGE: int = 31536000
    SECURITY_FRAME_DENY: bool = True
    SECURITY_XSS_PROTECTION: bool = True
    SECURITY_CONTENT_TYPE_OPTIONS: bool = True

    #######################################
    # Docker Configuration
    #######################################
    DOCKER_REGISTRY: str = "local"  # Single definition
    DOCKER_IMAGE_TAG: str = "latest"
    DOCKER_BUILD_VERSION: str = "latest"

    # Resource Limits
    CONTAINER_CPU_LIMIT: str = "1"
    CONTAINER_MEMORY_LIMIT: str = "512M"
    CONTAINER_CPU_RESERVATION: str = "0.25"
    CONTAINER_MEMORY_RESERVATION: str = "256M"

    #######################################
    # Monitoring Configuration
    #######################################
    METRICS_ENABLED: bool = True
    METRICS_PORT: int = 9090
    METRICS_PATH: str = "/metrics"

    GRAFANA_USER: str = "admin"
    GRAFANA_PASSWORD: str = "admin"
    GRAFANA_PORT: int = 3000
    GRAFANA_PLUGINS: str = "grafana-piechart-panel"

    #######################################
    # Test Configuration
    #######################################
    TEST_DB_HOST: str = "localhost"
    TEST_DB_PORT: int = 5432
    TEST_DB_USER: str = "user"
    TEST_DB_PASSWORD: str = "password"
    TEST_DB_NAME: str = "test_db"
    TEST_DATABASE_URL: str | None = None

    TEST_REDIS_HOST: str = "localhost"
    TEST_REDIS_PORT: int = 6379
    TEST_REDIS_PASSWORD: str = "redis"
    TEST_REDIS_DB: int = 1
    TEST_REDIS_URL: str | None = None

    #######################################
    # Feature Flags
    #######################################
    FEATURE_ASYNC_TASKS: bool = True
    FEATURE_CACHE_ENABLED: bool = True
    FEATURE_API_DOCS: bool = True

    class Config:
        env_file = find_env_file()
        case_sensitive = True
        extra = "allow"  # Allow extra fields from env file

        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str) -> list[str] | bool | str:
            """
            Parse environment variables with special handling for certain fields.

            Args:
                field_name: The name of the environment variable
                raw_val: The raw value of the environment variable

            Returns:
                list[str] | bool | str: Parsed value of the environment variable
            """
            if field_name == "CORS_ALLOWED_ORIGINS":
                try:
                    result = json.loads(raw_val)
                    return cast(list[str], result)
                except json.JSONDecodeError:
                    if raw_val == "*":
                        return ["*"]
                    return [origin.strip() for origin in raw_val.split(",")]
            elif any(
                field_name.startswith(prefix)
                for prefix in [
                    "APP_DEBUG",
                    "REDIS_SSL",
                    "SECURITY_",
                    "FEATURE_",
                    "METRICS_ENABLED",
                ]
            ):
                return str(raw_val).lower() in ("true", "1", "t", "y", "yes")
            return raw_val

    def __init__(self, **kwargs: Any) -> None:
        """
        Initialize Settings with environment variables and computed values.

        Args:
            **kwargs: Keyword arguments to pass to parent class
        """
        super().__init__(**kwargs)

        # Construct DATABASE_URL if not explicitly set
        if self.DATABASE_URL is None:
            self.DATABASE_URL = (
                f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}"
                f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
            )

        # Construct REDIS_URL if not explicitly set
        if self.REDIS_URL is None:
            self.REDIS_URL = (
                f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:"
                f"{self.REDIS_PORT}/{self.REDIS_DB}"
            )

        # Construct test URLs if not explicitly set
        if self.TEST_DATABASE_URL is None:
            self.TEST_DATABASE_URL = (
                f"postgresql://{self.TEST_DB_USER}:{self.TEST_DB_PASSWORD}"
                f"@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"
            )

        if self.TEST_REDIS_URL is None:
            self.TEST_REDIS_URL = (
                f"redis://:{self.TEST_REDIS_PASSWORD}@{self.TEST_REDIS_HOST}:"
                f"{self.TEST_REDIS_PORT}/{self.TEST_REDIS_DB}"
            )


settings = Settings()

if __name__ == "__main__":
    env_file_path = Settings.Config.env_file
    logger.info(
        "Environment configuration - File: %s, Exists: %s",
        env_file_path,
        os.path.exists(env_file_path),
    )
