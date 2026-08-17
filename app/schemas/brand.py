from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class BrandBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    logo: Optional[str] = None
    is_verified: bool = False

class BrandCreate(BrandBase):
    pass

class BrandResponse(BrandBase):
    id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True
