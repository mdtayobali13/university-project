from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class CouponBase(BaseModel):
    code: str
    discount_type: str
    discount_value: float
    min_order_amount: Optional[float] = None
    max_discount_amount: Optional[float] = None
    start_date: datetime
    end_date: datetime
    usage_limit: Optional[int] = None
    per_user_limit: Optional[int] = None
    vendor_id: Optional[UUID] = None
    is_active: bool = True

class CouponCreate(CouponBase):
    pass

class CouponUpdate(BaseModel):
    code: Optional[str] = None
    discount_type: Optional[str] = None
    discount_value: Optional[float] = None
    min_order_amount: Optional[float] = None
    max_discount_amount: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    usage_limit: Optional[int] = None
    per_user_limit: Optional[int] = None
    vendor_id: Optional[UUID] = None
    is_active: Optional[bool] = None

class CouponResponse(CouponBase):
    id: UUID
    usage_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True
