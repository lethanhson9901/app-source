## /home/son/Documents/note/project/ci-cd-setup/app-source/src/__init__.py

```python
```

## /home/son/Documents/note/project/ci-cd-setup/app-source/src/code-generated.py

```python
```

## /home/son/Documents/note/project/ci-cd-setup/app-source/src/tests/__init__.py

```python
```

## /home/son/Documents/note/project/ci-cd-setup/app-source/src/tests/check_forbidden_words.py

```python
"""Check for forbidden words in Python files."""
import re
import sys
from typing import List, Pattern

FORBIDDEN_PATTERNS: List[Pattern] = [
    re.compile(r"# FIXME\b"),
    re.compile(r"# TODO\b"),
    re.compile(r"print\("),  # Prevent print statements in production code
    re.compile(r"breakpoint\(\)"),  # Prevent debugger statements
]


def check_file(filename: str) -> List[str]:
    """Check a file for forbidden patterns."""
    errors = []
    with open(filename, "r", encoding="utf-8") as file:
        for i, line in enumerate(file, start=1):
            for pattern in FORBIDDEN_PATTERNS:
                if pattern.search(line):
                    errors.append(
                        f"{filename}:{i}: Found forbidden pattern: {line.strip()}"
                    )
    return errors


def main() -> int:
    """Main function."""
    errors = []
    for filename in sys.argv[1:]:
        errors.extend(check_file(filename))

    if errors:
        print("\n".join(errors))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

## /home/son/Documents/note/project/ci-cd-setup/app-source/src/tests/conftest.py

```python
import asyncio
import os
import sys
from pathlib import Path
from typing import Generator

import pytest
from fastapi.testclient import TestClient

project_root = str(Path(__file__).parent.parent.parent)
sys.path.insert(0, project_root)

from src.app.config import settings  # noqa: E402
from src.app.main import app  # noqa: E402

os.environ["ENVIRONMENT"] = "test"


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def test_app():
    """Create a test instance of the FastAPI application."""
    return app


@pytest.fixture(scope="session")
def client(test_app):
    """Create a test client using the test application."""
    with TestClient(test_app) as test_client:
        yield test_client


@pytest.fixture(scope="session")
def test_settings():
    """Provide test settings."""
    return settings


@pytest.fixture(autouse=True)
def setup_env():
    """Setup test environment variables before each test."""
    original_env = dict(os.environ)

    test_env = {
        "ENVIRONMENT": "test",
        "DEBUG": "true",
        "DATABASE_URL": "postgresql://test:test@localhost:5432/test_db",
        "REDIS_URL": "redis://localhost:6379/1",
    }
    os.environ.update(test_env)

    yield

    os.environ.clear()
    os.environ.update(original_env)
```

## /home/son/Documents/note/project/ci-cd-setup/app-source/src/tests/integration/__init__.py

```python
```

## /home/son/Documents/note/project/ci-cd-setup/app-source/src/tests/integration/test_api.py

```python
```

## /home/son/Documents/note/project/ci-cd-setup/app-source/src/tests/integration/test_database.py

```python
```

## /home/son/Documents/note/project/ci-cd-setup/app-source/src/tests/integration/test_redis.py

```python
```

## /home/son/Documents/note/project/ci-cd-setup/app-source/src/tests/e2e/__init__.py

```python
```

## /home/son/Documents/note/project/ci-cd-setup/app-source/src/tests/e2e/test_workflow.py

```python
```

## /home/son/Documents/note/project/ci-cd-setup/app-source/src/tests/unit/__init__.py

```python
```

## /home/son/Documents/note/project/ci-cd-setup/app-source/src/tests/unit/test_health.py

```python










import pytest
from unittest.mock import Mock


@pytest.mark.unit
def test_health_check():
    """Test the health check endpoint."""
    response = Mock()
    response.status_code = 200
    response.json.return_value = {"status": "ok"}

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.unit
def test_health_check_ready():
    """Test the readiness check endpoint."""
    response = Mock()
    response.status_code = 200
    response.json.return_value = {
        "status": "ready",
        "checks": {"database": True, "redis": True, "api": True},
    }

    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "checks" in data
    assert isinstance(data["checks"], dict)
```

## /home/son/Documents/note/project/ci-cd-setup/app-source/src/app/__init__.py

```python
```

## /home/son/Documents/note/project/ci-cd-setup/app-source/src/app/config.py

```python
import json
import os
from pathlib import Path
from typing import Any, cast

from pydantic_settings import BaseSettings


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

    Returns:
        str: The appropriate host binding
    """
    env = os.getenv("APP_ENVIRONMENT", "development")
    if env in ["production", "container"]:
        return "0.0.0.0"  # nosec B104 # Required for production/container environment
    return "127.0.0.1"  # Default to localhost for security


class Settings(BaseSettings):
    APP_NAME: str = "Python Application"
    APP_VERSION: str = "1.0.0"
    APP_ENVIRONMENT: str = "development"
    APP_DEBUG: bool = False
    APP_HOST: str = get_default_host()
    APP_PORT: int = 8080
    APP_LOG_LEVEL: str = "INFO"

    API_KEY: str = "dev-secret-key"
    API_RATE_LIMIT: str = "100/minute"
    API_TIMEOUT: int = 30

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

    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = "redis"
    REDIS_DB: int = 0
    REDIS_SSL: bool = False
    REDIS_TIMEOUT: int = 5
    REDIS_URL: str | None = None

    CORS_ALLOWED_ORIGINS: list[str] = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_MAX_AGE: int = 3600

    SECURITY_HSTS_ENABLED: bool = True
    SECURITY_HSTS_MAX_AGE: int = 31536000
    SECURITY_FRAME_DENY: bool = True
    SECURITY_XSS_PROTECTION: bool = True
    SECURITY_CONTENT_TYPE_OPTIONS: bool = True

    DOCKER_REGISTRY: str = "local"
    DOCKER_IMAGE_TAG: str = "latest"
    DOCKER_BUILD_VERSION: str = "latest"

    CONTAINER_CPU_LIMIT: str = "1"
    CONTAINER_MEMORY_LIMIT: str = "512M"
    CONTAINER_CPU_RESERVATION: str = "0.25"
    CONTAINER_MEMORY_RESERVATION: str = "256M"

    METRICS_ENABLED: bool = True
    METRICS_PORT: int = 9090
    METRICS_PATH: str = "/metrics"

    GRAFANA_USER: str = "admin"
    GRAFANA_PASSWORD: str = "admin"
    GRAFANA_PORT: int = 3000
    GRAFANA_PLUGINS: str = "grafana-piechart-panel"

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

    FEATURE_ASYNC_TASKS: bool = True
    FEATURE_CACHE_ENABLED: bool = True
    FEATURE_API_DOCS: bool = True

    class Config:
        env_file = find_env_file()
        case_sensitive = True

        @classmethod
        def parse_env_var(
            cls, field_name: str, raw_val: str
        ) -> list[str] | bool | str:  # Changed from Union
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

        if self.DATABASE_URL is None:
            self.DATABASE_URL = (
                f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}"
                f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
            )

        if self.REDIS_URL is None:
            self.REDIS_URL = (
                f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:"
                f"{self.REDIS_PORT}/{self.REDIS_DB}"
            )

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
    print(f"\nUsing .env file: {env_file_path}")
    print(f"File exists: {os.path.exists(env_file_path)}")
```

## /home/son/Documents/note/project/ci-cd-setup/app-source/src/app/dependencies.py

```python
from collections.abc import AsyncGenerator
from typing import cast

import redis.asyncio as redis

from asyncpg import connect
from asyncpg.connection import Connection
from redis.asyncio.client import Redis

from .config import Settings, settings

Connection = Connection  # type: ignore


async def get_db() -> AsyncGenerator[Connection, None]:
    """
    Create and yield a database connection.

    Returns:
        AsyncGenerator[Connection, None]: Database connection

    Raises:
        asyncpg.exceptions.PostgresError: If connection fails
    """
    conn: Connection = await connect(settings.DATABASE_URL)
    try:
        yield conn
    finally:
        await conn.close()


async def get_redis() -> AsyncGenerator[Redis, None]:
    """
    Create and yield a Redis connection.

    Returns:
        AsyncGenerator[Redis, None]: Redis connection

    Raises:
        redis.exceptions.RedisError: If connection fails
    """
    redis_client: Redis = cast(Redis, redis.from_url(settings.REDIS_URL))
    try:
        yield redis_client
    finally:
        await redis_client.close()


def get_settings() -> Settings:
    """
    Get application settings.

    Returns:
        Settings: Application settings configuration
    """
    return settings
```

## /home/son/Documents/note/project/ci-cd-setup/app-source/src/app/main.py

```python
import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from .api import health, views
from .config import settings
from .middleware import LoggingMiddleware, MetricsMiddleware

logger = structlog.get_logger(__name__)
tracer = trace.get_tracer(__name__)


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME, version=settings.APP_VERSION, debug=settings.APP_DEBUG
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(MetricsMiddleware)
    app.add_middleware(LoggingMiddleware)

    app.include_router(health.router)
    app.include_router(views.router)

    FastAPIInstrumentor.instrument_app(app)

    @app.get("/")
    async def root():
        return {
            "name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "environment": settings.APP_ENVIRONMENT,
        }

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.APP_DEBUG,
        log_level=settings.APP_LOG_LEVEL.lower(),
    )
```

## /home/son/Documents/note/project/ci-cd-setup/app-source/src/app/middleware.py

```python
import time
from collections.abc import Callable

import structlog
from fastapi import Request
from prometheus_client import Histogram
from starlette.middleware.base import BaseHTTPMiddleware

logger = structlog.get_logger(__name__)

request_duration = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"],
)


class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time

        request_duration.labels(
            method=request.method, endpoint=request.url.path
        ).observe(duration)

        return response


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        logger.info(
            "request_started",
            method=request.method,
            path=request.url.path,
            client_ip=request.client.host,
        )

        try:
            response = await call_next(request)
            logger.info(
                "request_completed",
                method=request.method,
                path=request.url.path,
                status_code=response.status_code,
            )
            return response
        except Exception as e:
            logger.error(
                "request_failed",
                method=request.method,
                path=request.url.path,
                error=str(e),
            )
            raise
```

## /home/son/Documents/note/project/ci-cd-setup/app-source/src/app/models.py

```python
from datetime import datetime

from pydantic import BaseModel, Field


class Item(BaseModel):
    id: int
    name: str
    description: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True
```

## /home/son/Documents/note/project/ci-cd-setup/app-source/src/app/api/health.py

```python
from typing import Annotated

from fastapi import APIRouter, Depends
from prometheus_client import Counter

from ..dependencies import get_db

router = APIRouter(tags=["health"])
health_check_counter = Counter("health_check_total", "Total health check requests")

DBDependency = Annotated[get_db, Depends(get_db)]


@router.get("/health/live")
async def liveness():
    health_check_counter.inc()
    return {"status": "alive"}


@router.get("/health/ready")
async def readiness(db: DBDependency):
    try:
        await db.execute("SELECT 1")
        return {"status": "ready"}
    except Exception as e:
        return {"status": "not ready", "error": str(e)}
```

## /home/son/Documents/note/project/ci-cd-setup/app-source/src/app/api/views.py

```python
from typing import Annotated

import structlog
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import APIKeyHeader

from ..config import settings
from ..dependencies import get_db
from ..models import Item

logger = structlog.get_logger(__name__)
router = APIRouter(prefix="/api/v1")
api_key_header = APIKeyHeader(name="X-API-Key")

DBDependency = Annotated[get_db, Depends(get_db)]
APIKeyDependency = Annotated[str, Depends(api_key_header)]


@router.get("/items", response_model=list[Item])
async def get_items(
    db: DBDependency,
    api_key: APIKeyDependency,
    skip: int = 0,
    limit: int = 10,
):
    if api_key != settings.API_KEY:
        logger.error("invalid_api_key", key=api_key)
        raise HTTPException(status_code=403, detail="Invalid API key")

    items = await db.fetch_all(
        "SELECT * FROM items OFFSET :skip LIMIT :limit", {"skip": skip, "limit": limit}
    )
    return items
```
