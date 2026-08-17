from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List
from app.core.database import get_db
from app.schemas.engagement import ReviewCreate, ReviewResponse, NotificationResponse, DeliveryUpdate, DeliveryResponse
from app.schemas.common import StandardResponse
from app.services.engagement_service import EngagementService

router = APIRouter() 
# --- REVIEWS ---
@router.post("/reviews", response_model=StandardResponse[ReviewResponse])
async def add_review(
    review_in: ReviewCreate, 
    user_id: UUID, 
    db: AsyncSession = Depends(get_db)
):
    service = EngagementService(db)
    review = await service.create_review(user_id, review_in)
    return StandardResponse(success=True, message="Review added", data=review)

@router.get("/reviews/{product_id}", response_model=StandardResponse[List[ReviewResponse]])
async def get_reviews(product_id: UUID, db: AsyncSession = Depends(get_db)):
    service = EngagementService(db)
    reviews = await service.get_product_reviews(product_id)
    return StandardResponse(success=True, message="Reviews retrieved", data=reviews)

# --- NOTIFICATIONS ---
@router.get("/notifications/{user_id}", response_model=StandardResponse[List[NotificationResponse]])
async def get_notifications(user_id: UUID, db: AsyncSession = Depends(get_db)):
    service = EngagementService(db)
    notifications = await service.get_user_notifications(user_id)
    return StandardResponse(success=True, message="Notifications retrieved", data=notifications)

@router.patch("/notifications/{notification_id}/read")
async def mark_read(notification_id: UUID, db: AsyncSession = Depends(get_db)):
    service = EngagementService(db)
    await service.mark_notification_read(notification_id)
    return {"success": True, "message": "Notification marked as read"}

# --- DELIVERIES ---
@router.patch("/deliveries/{delivery_id}/status", response_model=StandardResponse[DeliveryResponse])
async def update_delivery(
    delivery_id: UUID, 
    update_data: DeliveryUpdate, 
    agent_id: UUID, # Assume from auth
    db: AsyncSession = Depends(get_db)
):
    service = EngagementService(db)
    delivery = await service.update_delivery_status(delivery_id, agent_id, update_data)
    return StandardResponse(success=True, message="Delivery status updated", data=delivery)
