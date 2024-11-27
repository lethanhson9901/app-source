import structlog
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import APIKeyHeader

from ..config import settings
from ..models import Item

logger = structlog.get_logger(__name__)
router = APIRouter(prefix="/api/v1")
api_key_header = APIKeyHeader(name="X-API-Key")

# In-memory storage
items_db = []
current_id = 0


@router.post("/items", response_model=Item)
async def create_item(item: Item, api_key: str = Depends(api_key_header)):
    if api_key != settings.API_KEY:
        logger.error("invalid_api_key", key=api_key)
        raise HTTPException(status_code=403, detail="Invalid API key")

    global current_id
    current_id += 1
    item.id = current_id
    items_db.append(item)
    return item


@router.get("/items", response_model=list[Item])
async def get_items(
    api_key: str = Depends(api_key_header),
    skip: int = 0,
    limit: int = 10,
):
    if api_key != settings.API_KEY:
        logger.error("invalid_api_key", key=api_key)
        raise HTTPException(status_code=403, detail="Invalid API key")

    return items_db[skip : skip + limit]


@router.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item, api_key: str = Depends(api_key_header)):
    if api_key != settings.API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")

    for idx, existing_item in enumerate(items_db):
        if existing_item.id == item_id:
            item.id = item_id
            items_db[idx] = item
            return item
    raise HTTPException(status_code=404, detail="Item not found")


@router.delete("/items/{item_id}")
async def delete_item(item_id: int, api_key: str = Depends(api_key_header)):
    if api_key != settings.API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")

    for idx, item in enumerate(items_db):
        if item.id == item_id:
            items_db.pop(idx)
            return {"message": "Item deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")
