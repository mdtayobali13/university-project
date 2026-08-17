from sqlalchemy import Column, String, Numeric, Integer, ForeignKey, Enum, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import BaseModel
import enum

class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    PACKED = "packed"
    SHIPPED = "shipped"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    RETURNED = "returned"
    REFUNDED = "refunded"

class Order(BaseModel):
    """Parent order created by the customer during checkout"""
    __tablename__ = "orders"
    
    user_id = Column(ForeignKey("users.id"), nullable=False)
    address_id = Column(ForeignKey("addresses.id"), nullable=False)
    coupon_id = Column(ForeignKey("coupons.id"), nullable=True)
    
    total_amount = Column(Numeric(10, 2), nullable=False)
    discount_amount = Column(Numeric(10, 2), default=0.0)
    shipping_fee = Column(Numeric(10, 2), default=0.0)
    tax_amount = Column(Numeric(10, 2), default=0.0)
    grand_total = Column(Numeric(10, 2), nullable=False)
    
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    payment_status = Column(String, default="pending") # pending, paid, failed, refunded
    payment_method = Column(String, nullable=True)
    
    vendor_orders = relationship("VendorOrder", back_populates="parent_order", cascade="all, delete-orphan")
    status_history = relationship("OrderStatusHistory", back_populates="order", cascade="all, delete-orphan")

class VendorOrder(BaseModel):
    """Sub-order split by vendor for multi-vendor checkout"""
    __tablename__ = "vendor_orders"
    
    parent_order_id = Column(ForeignKey("orders.id"), nullable=False)
    vendor_id = Column(ForeignKey("vendors.id"), nullable=False)
    
    subtotal = Column(Numeric(10, 2), nullable=False)
    shipping_fee = Column(Numeric(10, 2), default=0.0)
    discount_amount = Column(Numeric(10, 2), default=0.0)
    total_amount = Column(Numeric(10, 2), nullable=False)
    
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    
    parent_order = relationship("Order", back_populates="vendor_orders")
    items = relationship("OrderItem", back_populates="vendor_order", cascade="all, delete-orphan")

class OrderItem(BaseModel):
    __tablename__ = "order_items"
    
    vendor_order_id = Column(ForeignKey("vendor_orders.id"), nullable=False)
    product_id = Column(ForeignKey("products.id"), nullable=False)
    variation_id = Column(ForeignKey("product_variations.id"), nullable=True)
    
    quantity = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False) # Price at the time of purchase
    
    vendor_order = relationship("VendorOrder", back_populates="items")
    product = relationship("Product")

class OrderStatusHistory(BaseModel):
    __tablename__ = "order_status_history"
    
    order_id = Column(ForeignKey("orders.id"), nullable=False)
    previous_status = Column(String, nullable=True)
    new_status = Column(String, nullable=False)
    changed_by_id = Column(ForeignKey("users.id"), nullable=True) # Admin/User who changed it
    note = Column(Text, nullable=True)
    
    order = relationship("Order", back_populates="status_history")
