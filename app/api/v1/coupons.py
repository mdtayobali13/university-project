from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID
from app.core.database import get_db
from app.schemas.coupon import CouponCreate, CouponUpdate, CouponResponse
from app.schemas.common import StandardResponse
from app.services.coupon_service import CouponService
from app.api.deps import get_current_active_user
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=StandardResponse[List[CouponResponse]])
async def get_coupons(db: AsyncSession = Depends(get_db)):
    coupon_service = CouponService(db)
    coupons = await coupon_service.get_all_coupons()
    return StandardResponse(success=True, message="Coupons retrieved", data=coupons)

@router.post("/", response_model=StandardResponse[CouponResponse])
async def create_coupon(
    coupon_in: CouponCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    coupon_service = CouponService(db)
    coupon = await coupon_service.create_coupon(coupon_in)
    return StandardResponse(success=True, message="Coupon created", data=coupon)

@router.patch("/{coupon_id}", response_model=StandardResponse[CouponResponse])
async def update_coupon(
    coupon_id: UUID,
    coupon_in: CouponUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    coupon_service = CouponService(db)
    coupon = await coupon_service.update_coupon(coupon_id, coupon_in)
    return StandardResponse(success=True, message="Coupon updated", data=coupon)

@router.delete("/{coupon_id}", response_model=StandardResponse[None])
async def delete_coupon(
    coupon_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    coupon_service = CouponService(db)
    await coupon_service.delete_coupon(coupon_id)
    return StandardResponse(success=True, message="Coupon deleted", data=None)

