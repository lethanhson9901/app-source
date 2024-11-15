import pytest
from fastapi.testclient import TestClient
from typing import Generator
import asyncio
import os
import sys
from pathlib import Path

# Add the project root directory to PYTHONPATH
project_root = str(Path(__file__).parent.parent.parent)
sys.path.insert(0, project_root)

from src.app.main import app
from src.app.config import settings

# Set test environment
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
    
    # Set test-specific environment variables
    test_env = {
        "ENVIRONMENT": "test",
        "DEBUG": "true",
        "DATABASE_URL": "postgresql://test:test@localhost:5432/test_db",
        "REDIS_URL": "redis://localhost:6379/1",
    }
    os.environ.update(test_env)
    
    yield
    
    # Restore original environment variables
    os.environ.clear()
    os.environ.update(original_env)