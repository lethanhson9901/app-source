import structlog
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import APIKeyHeader

from ..config import settings
from ..models import Item

logger = structlog.get_logger(__name__)
router = APIRouter(prefix="/api/v1")
api_key_header = APIKeyHeader(name="X-API-Key")


class ItemsRepository:
    def __init__(self) -> None:
        self._items: list[Item] = []
        self._current_id: int = 0

    def add_item(self, item: Item) -> Item:
        self._current_id += 1
        item.id = self._current_id
        self._items.append(item)
        return item

    def get_items(self, skip: int = 0, limit: int = 10) -> list[Item]:
        return self._items[skip : skip + limit]

    def update_item(self, item_id: int, updated_item: Item) -> Item | None:
        for idx, existing_item in enumerate(self._items):
            if existing_item.id == item_id:
                updated_item.id = item_id
                self._items[idx] = updated_item
                return updated_item
        return None

    def delete_item(self, item_id: int) -> bool:
        for idx, item in enumerate(self._items):
            if item.id == item_id:
                self._items.pop(idx)
                return True
        return False


# Create a single instance of the repository
items_repo = ItemsRepository()


def verify_api_key(api_key: str = Depends(api_key_header)) -> str:
    if api_key != settings.API_KEY:
        logger.error("invalid_api_key", key=api_key)
        raise HTTPException(status_code=403, detail="Invalid API key")
    return api_key


@router.post("/items", response_model=Item)
async def create_item(item: Item, _: str = Depends(verify_api_key)) -> Item:
    return items_repo.add_item(item)


@router.get("/items", response_model=list[Item])
async def get_items(
    skip: int = 0,
    limit: int = 10,
    _: str = Depends(verify_api_key),
) -> list[Item]:
    return items_repo.get_items(skip, limit)


@router.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item, _: str = Depends(verify_api_key)) -> Item:
    updated_item = items_repo.update_item(item_id, item)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item


@router.delete("/items/{item_id}")
async def delete_item(item_id: int, _: str = Depends(verify_api_key)) -> dict[str, str]:
    if not items_repo.delete_item(item_id):
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}
