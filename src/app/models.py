# src/app/models.py
from datetime import datetime

from pydantic import BaseModel, Field


class Item(BaseModel):
    id: int
    name: str
    description: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True
