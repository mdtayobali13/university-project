from sqlalchemy import Column, ForeignKey, Integer, Numeric
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Cart(BaseModel):
    __tablename__ = "carts"
    
    user_id = Column(ForeignKey("users.id"), unique=True, nullable=False)
    
    items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")

class CartItem(BaseModel):
    __tablename__ = "cart_items"
    
    cart_id = Column(ForeignKey("carts.id"), nullable=False)
    product_id = Column(ForeignKey("products.id"), nullable=False)
    variation_id = Column(ForeignKey("product_variations.id"), nullable=True)
    quantity = Column(Integer, default=1, nullable=False)
    
    cart = relationship("Cart", back_populates="items")
    product = relationship("Product")
    variation = relationship("ProductVariation")
