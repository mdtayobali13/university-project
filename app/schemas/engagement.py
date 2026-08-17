from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class ReviewCreate(BaseModel):
    product_id: UUID
    order_id: Optional[UUID] = None
    rating: int = Field(..., ge=1, le=5)
    review_text: Optional[str] = None
    images: Optional[str] = None

class ReviewResponse(BaseModel):
    id: UUID
    user_id: UUID
    product_id: UUID
    rating: int
    review_text: Optional[str]
    vendor_response: Optional[str]
    is_verified_purchase: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class NotificationResponse(BaseModel):
    id: UUID
    title: str
    message: str
    type: str
    is_read: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class DeliveryUpdate(BaseModel):
    status: str
    delivery_notes: Optional[str] = None

class DeliveryResponse(BaseModel):
    id: UUID
    order_id: UUID
    agent_id: UUID
    status: str
    tracking_number: str
    delivery_notes: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True
