# src/app/api/views.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import APIKeyHeader
from typing import List, Optional
from ..models import Item
from ..dependencies import get_db
from ..config import settings
import structlog

logger = structlog.get_logger(__name__)
router = APIRouter(prefix="/api/v1")
api_key_header = APIKeyHeader(name="X-API-Key")

@router.get("/items", response_model=List[Item])
async def get_items(
    skip: int = 0,
    limit: int = 10,
    db=Depends(get_db),
    api_key: str = Depends(api_key_header)
):
    if api_key != settings.API_KEY:
        logger.error("invalid_api_key", key=api_key)
        raise HTTPException(status_code=403, detail="Invalid API key")
    
    items = await db.fetch_all(
        "SELECT * FROM items OFFSET :skip LIMIT :limit",
        {"skip": skip, "limit": limit}
    )
    return items