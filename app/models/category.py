from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Category(BaseModel):
    __tablename__ = "categories"
    
    name = Column(String, unique=True, index=True, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    image = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    parent_id = Column(ForeignKey("categories.id"), nullable=True)
    
    subcategories = relationship("Category", backref="parent", remote_side="Category.id")
    products = relationship("Product", back_populates="category")
