from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime
from app.models.vendor import VendorStatus

class VendorBase(BaseModel):
    store_name: str
    owner_name: str
    email: EmailStr
    phone: str
    address: str
    business_info: Optional[Dict[str, Any]] = None
    bank_info: Optional[Dict[str, Any]] = None
    store_logo: Optional[str] = None
    store_banner: Optional[str] = None

class VendorCreate(VendorBase):
    pass

class VendorResponse(VendorBase):
    id: UUID
    user_id: UUID
    status: VendorStatus
    created_at: datetime
    
    class Config:
        from_attributes = True
