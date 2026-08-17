from sqlalchemy import Column, String, Numeric, Integer, DateTime, Boolean, ForeignKey
from app.models.base import BaseModel

class Coupon(BaseModel):
    __tablename__ = "coupons"
    
    code = Column(String, unique=True, index=True, nullable=False)
    discount_type = Column(String, nullable=False) # percentage, fixed
    discount_value = Column(Numeric(10, 2), nullable=False)
    min_order_amount = Column(Numeric(10, 2), nullable=True)
    max_discount_amount = Column(Numeric(10, 2), nullable=True)
    
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    
    usage_limit = Column(Integer, nullable=True)
    usage_count = Column(Integer, default=0)
    per_user_limit = Column(Integer, nullable=True)
    
    vendor_id = Column(ForeignKey("vendors.id"), nullable=True) # if null, global platform coupon
    is_active = Column(Boolean, default=True)
