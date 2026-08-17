from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List
from app.core.database import get_db
from app.schemas.payout import PayoutRequest, PayoutResponse, CommissionResponse
from app.schemas.common import StandardResponse
from app.services.payout_service import PayoutService

router = APIRouter()

@router.get("/commissions/{vendor_id}", response_model=StandardResponse[List[CommissionResponse]])
async def get_commissions(vendor_id: UUID, db: AsyncSession = Depends(get_db)):
    payout_service = PayoutService(db)
    commissions = await payout_service.get_vendor_commissions(vendor_id)
    return StandardResponse(success=True, message="Commissions retrieved", data=commissions)

@router.post("/request/{vendor_id}", response_model=StandardResponse[PayoutResponse])
async def request_payout(vendor_id: UUID, request: PayoutRequest, db: AsyncSession = Depends(get_db)):
    payout_service = PayoutService(db)
    payout = await payout_service.request_payout(vendor_id, request)
    return StandardResponse(success=True, message="Payout requested", data=payout)
