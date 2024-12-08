import asyncio
import os
import secrets
import sys
from pathlib import Path
from typing import AsyncGenerator, Generator

import pytest
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.testclient import TestClient

# Add the project root directory to PYTHONPATH before importing local modules
project_root = str(Path(__file__).parent.parent.parent)
sys.path.insert(0, project_root)

# Load environment variables from .env.test file if it exists
env_file = Path(project_root) / ".env.test"
if env_file.exists():
    load_dotenv(env_file)
else:
    load_dotenv()  # Fallback to default .env

# Now we can import from our project
from src.app.config import Settings, settings  # noqa: E402
from src.app.db.session import Base, async_engine  # noqa: E402
from src.app.main import app  # noqa: E402

# Set test environment
os.environ["ENVIRONMENT"] = "test"


# Utility function for generating test credentials
def generate_test_value() -> str:
    """Generate a random string for test values."""
    return secrets.token_urlsafe(16)


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def test_app() -> FastAPI:
    """Create a test instance of the FastAPI application."""
    return app


@pytest.fixture(scope="session")
def client(test_app: FastAPI) -> Generator[TestClient, None, None]:
    """Create a test client using the test application."""
    with TestClient(test_app) as test_client:
        yield test_client


@pytest.fixture(scope="session")
def test_settings() -> Settings:
    """Provide test settings."""
    return settings


@pytest.fixture(autouse=True)
async def setup_test_db() -> AsyncGenerator[None, None]:
    """Setup test database tables before tests and cleanup after."""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(autouse=True)
def setup_env() -> Generator[None, None, None]:
    """Setup test environment variables before each test."""
    original_env = dict(os.environ)

    if not os.getenv("TEST_DATABASE_URL"):
        raise ValueError(
            "TEST_DATABASE_URL environment variable is required. "
            "Please set it in your .env.test file or environment."
        )

    # Set test-specific environment variables
    test_env = {
        "ENVIRONMENT": "test",
        "DEBUG": "true",
        "DATABASE_URL": os.environ["TEST_DATABASE_URL"],  # Require explicit test database URL
        "REDIS_URL": os.getenv("TEST_REDIS_URL", "redis://localhost:6379/1"),
        "API_KEY": os.getenv("TEST_API_KEY", generate_test_value()),
        "CORS_ALLOWED_ORIGINS": '["http://localhost:3000","http://localhost:8080"]',
        "CORS_ALLOW_CREDENTIALS": "true",
        "METRICS_ENABLED": "false",
        "FEATURE_ASYNC_TASKS": "false",
        "FEATURE_CACHE_ENABLED": "false",
    }
    os.environ.update(test_env)

    yield

    # Restore original environment variables
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def mock_settings(monkeypatch: pytest.MonkeyPatch) -> Generator[Settings, None, None]:
    """Provide a fixture for mocking settings."""
    test_settings = Settings(
        APP_NAME="Test App",
        APP_VERSION="1.0.0",
        APP_ENVIRONMENT="test",
        APP_DEBUG=True,
        APP_HOST="localhost",
        APP_PORT=8000,
        DATABASE_URL=os.environ["TEST_DATABASE_URL"],
        REDIS_URL=os.getenv("TEST_REDIS_URL", "redis://localhost:6379/1"),
    )

    monkeypatch.setattr("src.app.config.settings", test_settings)
    yield test_settings


@pytest.fixture
async def test_data() -> AsyncGenerator[dict, None]:
    """Provide test data that can be used across tests."""
    data = {
        "test_user": {
            "username": f"testuser_{generate_test_value()}",
            "email": f"test_{generate_test_value()}@example.com",
            "password": generate_test_value(),  # Generate random password for tests
        },
        "test_item": {
            "name": "Test Item",
            "description": "This is a test item",
            "price": 9.99,
        },
    }
    yield data


@pytest.fixture
def auth_headers() -> dict[str, str]:
    """Provide authentication headers for protected endpoints."""
    return {
        "Authorization": f"Bearer {os.environ['TEST_API_KEY']}",
        "Content-Type": "application/json",
    }


@pytest.fixture
async def cleanup_redis() -> AsyncGenerator[None, None]:
    """Clean up Redis test database before and after tests."""
    yield
    # Implement Redis cleanup logic here if needed
