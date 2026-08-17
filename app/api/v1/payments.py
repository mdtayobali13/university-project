from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.core.database import get_db
from app.schemas.payment import PaymentResponse
from app.schemas.common import StandardResponse
from app.services.payment_service import PaymentService
from pydantic import BaseModel

router = APIRouter()

class PaymentInitiateRequest(BaseModel):
    order_id: UUID
    gateway: str

@router.post("/initiate")
async def initiate_payment(
    request: PaymentInitiateRequest,
    user_id: UUID, # Assume from auth dependency
    db: AsyncSession = Depends(get_db)
):
    payment_service = PaymentService(db)
    result = await payment_service.initiate_payment(user_id, request.order_id, request.gateway)
    return StandardResponse(success=True, message="Payment initiated", data=result)

@router.post("/webhook/{gateway}")
async def handle_webhook(
    gateway: str,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    payload = await request.json()
    payment_service = PaymentService(db)
    await payment_service.handle_webhook(gateway, payload)
    return {"status": "success"}
