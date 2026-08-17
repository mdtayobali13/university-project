from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID

class DashboardAnalyticsResponse(BaseModel):
    total_users: int
    total_vendors: int
    total_products: int
    total_orders: int
    total_revenue: float
    platform_commission: float
    vendor_earnings: float
    pending_vendor_approvals: int
    pending_payouts: int

class ProductApprovalRequest(BaseModel):
    status: str # approved, rejected
    rejection_reason: Optional[str] = None
