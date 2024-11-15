# src/tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from asyncpg.pool import Pool
import asyncpg
import os
from ..app.main import create_app
from ..app.config import settings

@pytest.fixture
def app():
    return create_app()

@pytest.fixture
def client(app):
    return TestClient(app)

@pytest.fixture
async def db_pool():
    pool = await asyncpg.create_pool(
        settings.DATABASE_URL,
        min_size=2,
        max_size=10
    )
    yield pool
    await pool.close()