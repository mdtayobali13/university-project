from pydantic import BaseModel
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime
from app.models.payment import PaymentStatus

class PaymentCreate(BaseModel):
    order_id: UUID
    gateway: str
    amount: float
    currency: str = "BDT"

class PaymentResponse(BaseModel):
    id: UUID
    order_id: UUID
    user_id: UUID
    amount: float
    currency: str
    gateway: str
    transaction_id: Optional[str]
    status: PaymentStatus
    created_at: datetime
    
    class Config:
        from_attributes = True

class WebhookPayload(BaseModel):
    gateway: str
    event_type: str
    data: Dict[str, Any]
