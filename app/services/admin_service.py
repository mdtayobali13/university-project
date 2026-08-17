from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from app.models.user import User
from app.models.vendor import Vendor, VendorStatus
from app.models.product import Product, ProductStatus
from app.models.order import Order
from app.models.payout import Commission, Payout, PayoutStatus
from fastapi import HTTPException
from uuid import UUID

class AdminService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_dashboard_analytics(self):
        # Users
        users_count = await self.db.execute(select(func.count(User.id)))
        
        # Vendors
        vendors_count = await self.db.execute(select(func.count(Vendor.id)))
        pending_vendors = await self.db.execute(select(func.count(Vendor.id)).where(Vendor.status == VendorStatus.PENDING))
        
        # Products
        products_count = await self.db.execute(select(func.count(Product.id)))
        
        # Orders & Revenue
        orders_count = await self.db.execute(select(func.count(Order.id)))
        total_revenue = await self.db.execute(select(func.sum(Order.grand_total)))
        
        # Commissions & Earnings
        platform_commission = await self.db.execute(select(func.sum(Commission.platform_fee)))
        vendor_earnings = await self.db.execute(select(func.sum(Commission.net_earnings)))
        
        # Payouts
        pending_payouts = await self.db.execute(select(func.count(Payout.id)).where(Payout.status == PayoutStatus.PENDING))
        
        return {
            "total_users": users_count.scalar() or 0,
            "total_vendors": vendors_count.scalar() or 0,
            "total_products": products_count.scalar() or 0,
            "total_orders": orders_count.scalar() or 0,
            "total_revenue": float(total_revenue.scalar() or 0),
            "platform_commission": float(platform_commission.scalar() or 0),
            "vendor_earnings": float(vendor_earnings.scalar() or 0),
            "pending_vendor_approvals": pending_vendors.scalar() or 0,
            "pending_payouts": pending_payouts.scalar() or 0,
        }

    async def approve_vendor(self, vendor_id: UUID, is_approved: bool):
        query = select(Vendor).where(Vendor.id == vendor_id)
        result = await self.db.execute(query)
        vendor = result.scalar_one_or_none()
        if not vendor:
            raise HTTPException(status_code=404, detail="Vendor not found")
            
        vendor.status = VendorStatus.APPROVED if is_approved else VendorStatus.REJECTED
        await self.db.commit()
        return vendor

    async def approve_product(self, product_id: UUID, status: str, rejection_reason: str = None):
        query = select(Product).where(Product.id == product_id)
        result = await self.db.execute(query)
        product = result.scalar_one_or_none()
        
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
            
        product.status = ProductStatus(status)
        # Note: If rejected, we might want to store the reason in a separate table or field
        await self.db.commit()
        return product
