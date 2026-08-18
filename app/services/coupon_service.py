from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.coupon import Coupon
from app.schemas.coupon import CouponCreate, CouponUpdate
from fastapi import HTTPException
from uuid import UUID

class CouponService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_coupon(self, coupon_in: CouponCreate) -> Coupon:
        query = select(Coupon).where(Coupon.code == coupon_in.code)
        result = await self.db.execute(query)
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Coupon code already exists")
            
        coupon = Coupon(**coupon_in.model_dump())
        self.db.add(coupon)
        await self.db.commit()
        await self.db.refresh(coupon)
        return coupon

    async def get_all_coupons(self):
        query = select(Coupon)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_coupon(self, coupon_id: UUID) -> Coupon:
        query = select(Coupon).where(Coupon.id == coupon_id)
        result = await self.db.execute(query)
        coupon = result.scalar_one_or_none()
        if not coupon:
            raise HTTPException(status_code=404, detail="Coupon not found")
        return coupon

    async def update_coupon(self, coupon_id: UUID, coupon_in: CouponUpdate) -> Coupon:
        coupon = await self.get_coupon(coupon_id)
        update_data = coupon_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(coupon, field, value)
        await self.db.commit()
        await self.db.refresh(coupon)
        return coupon

    async def delete_coupon(self, coupon_id: UUID):
        coupon = await self.get_coupon(coupon_id)
        await self.db.delete(coupon)
        await self.db.commit()
        return True
