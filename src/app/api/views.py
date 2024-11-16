from typing import Annotated

import structlog
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import APIKeyHeader

from ..config import settings
from ..dependencies import get_db
from ..models import Item

logger = structlog.get_logger(__name__)
router = APIRouter(prefix="/api/v1")
api_key_header = APIKeyHeader(name="X-API-Key")

# Define dependency type annotations
DBDependency = Annotated[get_db, Depends(get_db)]
APIKeyDependency = Annotated[str, Depends(api_key_header)]


@router.get("/items", response_model=list[Item])
async def get_items(
    db: DBDependency,
    api_key: APIKeyDependency,
    skip: int = 0,
    limit: int = 10,
):
    if api_key != settings.API_KEY:
        logger.error("invalid_api_key", key=api_key)
        raise HTTPException(status_code=403, detail="Invalid API key")

    items = await db.fetch_all(
        "SELECT * FROM items OFFSET :skip LIMIT :limit", {"skip": skip, "limit": limit}
    )
    return items
