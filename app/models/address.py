from sqlalchemy import Column, String, Boolean, ForeignKey, Numeric
from app.models.base import BaseModel
from sqlalchemy.orm import relationship

class Address(BaseModel):
    __tablename__ = "addresses"
    
    user_id = Column(ForeignKey("users.id"), nullable=False)
    full_name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    country = Column(String, nullable=False, default="Bangladesh")
    division = Column(String, nullable=False)
    district = Column(String, nullable=False)
    upazila = Column(String, nullable=False)
    postal_code = Column(String, nullable=False)
    full_address = Column(String, nullable=False)
    latitude = Column(Numeric(9, 6), nullable=True)
    longitude = Column(Numeric(9, 6), nullable=True)
    address_type = Column(String, nullable=False, default="Home") # Home, Office, Other
    is_default = Column(Boolean, default=False)
    
    user = relationship("User")
