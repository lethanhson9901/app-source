# src/app/models.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True
