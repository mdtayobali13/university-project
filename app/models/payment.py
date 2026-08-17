from sqlalchemy import Column, String, Numeric, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
import enum

class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    PAID = "paid"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"
    PARTIALLY_REFUNDED = "partially_refunded"

class Payment(BaseModel):
    __tablename__ = "payments"
    
    order_id = Column(ForeignKey("orders.id"), unique=True, nullable=False)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String, default="BDT")
    
    gateway = Column(String, nullable=False) # e.g., 'stripe', 'sslcommerz', 'cod'
    transaction_id = Column(String, unique=True, nullable=True) # Gateway transaction ID
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    
    gateway_response = Column(JSON, nullable=True) # Store raw webhook data
    
    order = relationship("Order")
