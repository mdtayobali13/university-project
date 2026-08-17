from pydantic import BaseModel ,Optional
from uuid import UUID
from datetime import datetime
from app.schemas.product import ProductResponse

class WishlistCreate(BaseModel):
    product_id: UUID

class WishlistResponse(BaseModel):
    id: UUID
    user_id: UUID
    product_id: UUID
    product: Optional[ProductResponse] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
