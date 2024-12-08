from typing import Annotated

from asyncpg import Connection
from fastapi import APIRouter, Depends
from prometheus_client import Counter
from sqlalchemy.exc import SQLAlchemyError

from ..dependencies import get_db

router = APIRouter(tags=["health"])
health_check_counter = Counter("health_check_total", "Total health check requests")

# Define the return type for health check responses
HealthResponse = dict[str, str]

# Define dependency type annotation
DBConnection = Annotated[Connection, Depends(get_db)]


@router.get("/health/live", response_model=HealthResponse)
async def liveness() -> HealthResponse:
    health_check_counter.inc()
    return {"status": "alive"}


@router.get("/health/ready", response_model=HealthResponse)
async def readiness(db: DBConnection) -> HealthResponse:
    try:
        # Check DB connection
        await db.execute("SELECT 1")
        return {"status": "ready"}
    except SQLAlchemyError as e:
        # Log the specific database error here if needed
        return {"status": "not ready", "error": str(e)}
