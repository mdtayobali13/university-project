from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List
from app.core.database import get_db
from app.schemas.order import CheckoutRequest, OrderResponse
from app.schemas.common import StandardResponse
from app.services.order_service import OrderService

router = APIRouter()

@router.post("/checkout", response_model=StandardResponse[OrderResponse])
async def checkout(
    request: CheckoutRequest,
    user_id: UUID, # Assume from auth dependency
    db: AsyncSession = Depends(get_db)
):
    order_service = OrderService(db)
    order = await order_service.checkout(user_id, request)
    return StandardResponse(success=True, message="Order placed successfully", data=order)

@router.get("/{user_id}", response_model=StandardResponse[List[OrderResponse]])
async def get_user_orders(user_id: UUID, db: AsyncSession = Depends(get_db)):
    order_service = OrderService(db)
    orders = await order_service.get_user_orders(user_id)
    return StandardResponse(success=True, message="Orders retrieved", data=orders)
