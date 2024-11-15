from typing import Annotated

from fastapi import APIRouter, Depends
from prometheus_client import Counter

from ..dependencies import get_db

router = APIRouter(tags=["health"])
health_check_counter = Counter("health_check_total", "Total health check requests")

# Define dependency type annotation
DBDependency = Annotated[get_db, Depends(get_db)]


@router.get("/health/live")
async def liveness():
    health_check_counter.inc()
    return {"status": "alive"}


@router.get("/health/ready")
async def readiness(db: DBDependency):
    try:
        # Check DB connection
        await db.execute("SELECT 1")
        return {"status": "ready"}
    except Exception as e:
        return {"status": "not ready", "error": str(e)}
