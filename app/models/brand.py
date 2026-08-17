from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Brand(BaseModel):
    __tablename__ = "brands"
    
    name = Column(String, unique=True, index=True, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    logo = Column(String, nullable=True)
    is_verified = Column(Boolean, default=False)
    
    products = relationship("Product", back_populates="brand")
