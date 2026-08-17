from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Wishlist(BaseModel):
    __tablename__ = "wishlists"
    
    user_id = Column(ForeignKey("users.id"), nullable=False)
    product_id = Column(ForeignKey("products.id"), nullable=False)
    
    user = relationship("User")
    product = relationship("Product")
