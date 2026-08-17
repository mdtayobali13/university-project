from sqlalchemy import Column, String, Text, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
import enum

class VendorStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    SUSPENDED = "suspended"
    ACTIVE = "active"

class Vendor(BaseModel):
    __tablename__ = "vendors"
    
    user_id = Column(ForeignKey("users.id"), unique=True, nullable=False)
    store_name = Column(String, unique=True, index=True, nullable=False)
    owner_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=False)
    address = Column(Text, nullable=False)
    business_info = Column(JSON, nullable=True) # NID, registration, etc
    store_logo = Column(String, nullable=True)
    store_banner = Column(String, nullable=True)
    bank_info = Column(JSON, nullable=True)
    status = Column(Enum(VendorStatus), default=VendorStatus.PENDING)
    
    user = relationship("User", backref="vendor_profile")
    products = relationship("Product", back_populates="vendor")
