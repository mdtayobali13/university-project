from sqlalchemy import Column, String, Numeric, ForeignKey, Integer, Text, Boolean, Enum
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
import enum

class Review(BaseModel):
    __tablename__ = "reviews"
    
    product_id = Column(ForeignKey("products.id"), nullable=False)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    order_id = Column(ForeignKey("orders.id"), nullable=True) # Must be a verified purchase
    
    rating = Column(Integer, nullable=False) # 1-5
    review_text = Column(Text, nullable=True)
    images = Column(String, nullable=True) # JSON or comma-separated URLs
    
    vendor_response = Column(Text, nullable=True)
    is_verified_purchase = Column(Boolean, default=False)
    is_approved = Column(Boolean, default=True) # Admin moderation
    
    user = relationship("User")
    product = relationship("Product")

class NotificationType(str, enum.Enum):
    ORDER = "order"
    PAYMENT = "payment"
    SYSTEM = "system"
    PROMOTIONAL = "promotional"

class Notification(BaseModel):
    __tablename__ = "notifications"
    
    user_id = Column(ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    type = Column(Enum(NotificationType), default=NotificationType.SYSTEM)
    is_read = Column(Boolean, default=False)
    
    user = relationship("User")

class DeliveryStatus(str, enum.Enum):
    ASSIGNED = "assigned"
    PICKED_UP = "picked_up"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    FAILED = "failed"

class Delivery(BaseModel):
    __tablename__ = "deliveries"
    
    order_id = Column(ForeignKey("orders.id"), nullable=False)
    agent_id = Column(ForeignKey("users.id"), nullable=False) # Delivery agent
    
    status = Column(Enum(DeliveryStatus), default=DeliveryStatus.ASSIGNED)
    tracking_number = Column(String, unique=True, nullable=False)
    delivery_notes = Column(Text, nullable=True)
    
    order = relationship("Order")
    agent = relationship("User")
