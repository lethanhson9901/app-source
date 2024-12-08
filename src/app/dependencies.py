from collections.abc import AsyncGenerator
from typing import Any

import redis.asyncio as redis
from asyncpg import Connection as AsyncPGConnection
from redis.asyncio.client import Redis

from .config import Settings, settings


async def get_db() -> AsyncGenerator[AsyncPGConnection, None]:
    """
    Create and yield a database connection.

    Returns:
        AsyncGenerator[AsyncPGConnection, None]: Database connection

    Raises:
        asyncpg.exceptions.PostgresError: If connection fails
    """
    conn = await AsyncPGConnection.connect(settings.DATABASE_URL)
    try:
        yield conn
    finally:
        await conn.close()


async def get_redis() -> AsyncGenerator[Redis[Any], None]:
    """
    Create and yield a Redis connection.

    Returns:
        AsyncGenerator[Redis, None]: Redis connection

    Raises:
        redis.exceptions.RedisError: If connection fails
    """
    if settings.REDIS_URL is None:
        raise ValueError("REDIS_URL must be set")

    redis_client = redis.from_url(settings.REDIS_URL)
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
