from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from app.models.order import OrderStatus
from app.schemas.product import ProductResponse

class OrderItemResponse(BaseModel):
    id: UUID
    product_id: UUID
    variation_id: Optional[UUID]
    quantity: int
    price: float
    product: Optional[ProductResponse] = None
    
    class Config:
        from_attributes = True

class VendorOrderResponse(BaseModel):
    id: UUID
    vendor_id: UUID
    subtotal: float
    shipping_fee: float
    discount_amount: float
    total_amount: float
    status: OrderStatus
    items: List[OrderItemResponse] = []
    
    class Config:
        from_attributes = True

class OrderStatusHistoryResponse(BaseModel):
    id: UUID
    previous_status: Optional[str]
    new_status: str
    note: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    id: UUID
    user_id: UUID
    address_id: UUID
    total_amount: float
    discount_amount: float
    shipping_fee: float
    tax_amount: float
    grand_total: float
    status: OrderStatus
    payment_status: str
    payment_method: Optional[str]
    created_at: datetime
    vendor_orders: List[VendorOrderResponse] = []
    status_history: List[OrderStatusHistoryResponse] = []
    
    class Config:
        from_attributes = True

class CheckoutRequest(BaseModel):
    address_id: UUID
    payment_method: str
    coupon_code: Optional[str] = None
