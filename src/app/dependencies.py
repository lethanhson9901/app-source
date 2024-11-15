from typing import AsyncGenerator, cast

import redis.asyncio as redis
from redis.asyncio.client import Redis
# Use Any for asyncpg types since there are no stubs
from asyncpg import connect
from asyncpg.connection import Connection

from .config import Settings, settings

# Type ignore for asyncpg imports since they lack stubs
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