import os
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base

# Create declarative base instance
Base = declarative_base()


# Get database URL from environment variables
def get_database_url() -> str:
    """Get database URL from environment variables."""
    user = os.getenv("DB_USER", "user")
    password = os.getenv("DB_PASSWORD", "password")
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "dbname")

    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}"


# Create async engine instance
async_engine: AsyncEngine = create_async_engine(
    get_database_url(),
    echo=bool(os.getenv("APP_DEBUG", "false").lower() == "true"),
)


# Async session factory with correct return type hint
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Create and yield an async database session."""
    async with AsyncSession(async_engine) as session:
        yield session
