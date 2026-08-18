from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List
from app.core.database import get_db
from app.schemas.order import CheckoutRequest, OrderResponse
from app.schemas.common import StandardResponse
from app.services.order_service import OrderService
from app.api.deps import get_current_active_user
from app.models.user import User, UserRole

router = APIRouter()

def check_user_authorization(user_id: UUID, current_user: User):
    if current_user.id != user_id and current_user.role not in [UserRole.ADMIN, UserRole.SUPER_ADMIN]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access these orders")

@router.post("/checkout", response_model=StandardResponse[OrderResponse])
async def checkout(
    request: CheckoutRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    order_service = OrderService(db)
    order = await order_service.checkout(current_user.id, request)
    return StandardResponse(success=True, message="Order placed successfully", data=order)

@router.get("/{user_id}", response_model=StandardResponse[List[OrderResponse]])
async def get_user_orders(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    check_user_authorization(user_id, current_user)
    order_service = OrderService(db)
    orders = await order_service.get_user_orders(user_id)
    return StandardResponse(success=True, message="Orders retrieved", data=orders)

