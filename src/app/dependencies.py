import asyncpg
from fastapi import Depends
from .config import settings
import redis.asyncio as redis
from typing import AsyncGenerator

async def get_db() -> AsyncGenerator[asyncpg.Connection, None]:
    conn = await asyncpg.connect(settings.DATABASE_URL)
    try:
        yield conn
    finally:
        await conn.close()

async def get_redis() -> AsyncGenerator[redis.Redis, None]:
    redis_client = redis.from_url(settings.REDIS_URL)
    try:
        yield redis_client
    finally:
        await redis_client.close()

def get_settings():
    return settings