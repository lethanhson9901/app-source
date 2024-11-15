# src/app/api/health.py
from fastapi import APIRouter, Depends
from ..dependencies import get_db
from prometheus_client import Counter

router = APIRouter(tags=["health"])
health_check_counter = Counter('health_check_total', 'Total health check requests')

@router.get("/health/live")
async def liveness():
    health_check_counter.inc()
    return {"status": "alive"}

@router.get("/health/ready")
async def readiness(db=Depends(get_db)):
    try:
        # Check DB connection
        await db.execute("SELECT 1")
        return {"status": "ready"}
    except Exception as e:
        return {"status": "not ready", "error": str(e)}
    
