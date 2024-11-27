from datetime import datetime

from pydantic import BaseModel, Field


class Item(BaseModel):
    id: int | None = None
    name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True
