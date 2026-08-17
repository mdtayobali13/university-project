from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.models.payout import PayoutStatus

class CommissionResponse(BaseModel):
    id: UUID
    vendor_id: UUID
    vendor_order_id: UUID
    gross_amount: float
    platform_fee: float
    net_earnings: float
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class PayoutRequest(BaseModel):
    amount: float
    bank_account_info: str

class PayoutResponse(BaseModel):
    id: UUID
    vendor_id: UUID
    amount: float
    status: PayoutStatus
    bank_account_info: str
    transaction_id: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True
