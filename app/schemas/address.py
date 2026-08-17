from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class AddressBase(BaseModel):
    full_name: str
    phone: str
    country: str = "Bangladesh"
    division: str
    district: str
    upazila: str
    postal_code: str
    full_address: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    address_type: str = "Home"
    is_default: bool = False

class AddressCreate(AddressBase):
    pass

class AddressUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    division: Optional[str] = None
    district: Optional[str] = None
    upazila: Optional[str] = None
    postal_code: Optional[str] = None
    full_address: Optional[str] = None
    is_default: Optional[bool] = None

class AddressResponse(AddressBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True
