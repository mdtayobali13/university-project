from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from app.schemas.product import ProductResponse, ProductVariationResponse

class CartItemBase(BaseModel):
    product_id: UUID
    variation_id: Optional[UUID] = None
    quantity: int = 1

class CartItemCreate(CartItemBase):
    pass

class CartItemUpdate(BaseModel):
    quantity: int

class CartItemResponse(CartItemBase):
    id: UUID
    cart_id: UUID
    product: Optional[ProductResponse] = None
    variation: Optional[ProductVariationResponse] = None
    
    class Config:
        from_attributes = True

class CartResponse(BaseModel):
    id: UUID
    user_id: UUID
    items: List[CartItemResponse] = []
    
    class Config:
        from_attributes = True
