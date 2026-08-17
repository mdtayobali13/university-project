from sqlalchemy import Column, String, Numeric, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
import enum

class PayoutStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    PROCESSING = "processing"
    PAID = "paid"
    REJECTED = "rejected"

class Commission(BaseModel):
    __tablename__ = "commissions"
    
    vendor_order_id = Column(ForeignKey("vendor_orders.id"), unique=True, nullable=False)
    vendor_id = Column(ForeignKey("vendors.id"), nullable=False)
    
    gross_amount = Column(Numeric(10, 2), nullable=False)
    platform_fee = Column(Numeric(10, 2), nullable=False)
    net_earnings = Column(Numeric(10, 2), nullable=False)
    
    status = Column(String, default="pending") # pending, ready_for_payout, paid
    
    vendor = relationship("Vendor")
    vendor_order = relationship("VendorOrder")

class Payout(BaseModel):
    __tablename__ = "payouts"
    
    vendor_id = Column(ForeignKey("vendors.id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    status = Column(Enum(PayoutStatus), default=PayoutStatus.PENDING)
    
    bank_account_info = Column(Text, nullable=False)
    transaction_id = Column(String, nullable=True) # ID when paid
    
    vendor = relationship("Vendor")
