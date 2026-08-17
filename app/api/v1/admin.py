from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.core.database import get_db
from app.schemas.admin import DashboardAnalyticsResponse, ProductApprovalRequest
from app.schemas.common import StandardResponse
from app.services.admin_service import AdminService

router = APIRouter()

@router.get("/analytics", response_model=StandardResponse[DashboardAnalyticsResponse])
async def get_analytics(db: AsyncSession = Depends(get_db)):
    # Note: Requires Admin Role checking dependency in production
    admin_service = AdminService(db)
    data = await admin_service.get_dashboard_analytics()
    return StandardResponse(success=True, message="Analytics retrieved", data=data)

@router.patch("/vendors/{vendor_id}/approve")
async def approve_vendor(vendor_id: UUID, approved: bool = True, db: AsyncSession = Depends(get_db)):
    admin_service = AdminService(db)
    await admin_service.approve_vendor(vendor_id, approved)
    return {"success": True, "message": "Vendor status updated"}

@router.patch("/products/{product_id}/approve")
async def approve_product(product_id: UUID, request: ProductApprovalRequest, db: AsyncSession = Depends(get_db)):
    admin_service = AdminService(db)
    await admin_service.approve_product(product_id, request.status, request.rejection_reason)
    return {"success": True, "message": "Product status updated"}
