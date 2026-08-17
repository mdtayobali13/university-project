from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
from app.schemas.coupon import CouponCreate, CouponResponse
from app.schemas.common import StandardResponse
from app.services.coupon_service import CouponService

router = APIRouter()

@router.get("/", response_model=StandardResponse[List[CouponResponse]])
async def get_coupons(db: AsyncSession = Depends(get_db)):
    coupon_service = CouponService(db)
    coupons = await coupon_service.get_all_coupons()
    return StandardResponse(success=True, message="Coupons retrieved", data=coupons)

@router.post("/", response_model=StandardResponse[CouponResponse])
async def create_coupon(coupon_in: CouponCreate, db: AsyncSession = Depends(get_db)):
    coupon_service = CouponService(db)
    coupon = await coupon_service.create_coupon(coupon_in)
    return StandardResponse(success=True, message="Coupon created", data=coupon)
