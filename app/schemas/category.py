from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class CategoryBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    image: Optional[str] = None
    is_active: bool = True
    parent_id: Optional[UUID] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True
