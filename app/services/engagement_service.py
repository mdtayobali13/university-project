from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.engagement import Review, Notification, Delivery
from app.schemas.engagement import ReviewCreate, DeliveryUpdate
from fastapi import HTTPException
from uuid import UUID
import uuid

class EngagementService:
    def __init__(self, db: AsyncSession):
        self.db = db

    # --- REVIEWS ---
    async def create_review(self, user_id: UUID, review_in: ReviewCreate) -> Review:
        # Check if already reviewed
        query = select(Review).where(Review.user_id == user_id, Review.product_id == review_in.product_id)
        result = await self.db.execute(query)
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="You have already reviewed this product")
            
        review = Review(
            user_id=user_id,
            is_verified_purchase=review_in.order_id is not None,
            **review_in.model_dump()
        )
        self.db.add(review)
        await self.db.commit()
        await self.db.refresh(review)
        return review

    async def get_product_reviews(self, product_id: UUID):
        query = select(Review).where(Review.product_id == product_id, Review.is_approved == True)
        result = await self.db.execute(query)
        return result.scalars().all()

    # --- NOTIFICATIONS ---
    async def get_user_notifications(self, user_id: UUID):
        query = select(Notification).where(Notification.user_id == user_id).order_by(Notification.created_at.desc())
        result = await self.db.execute(query)
        return result.scalars().all()

    async def mark_notification_read(self, notification_id: UUID):
        query = select(Notification).where(Notification.id == notification_id)
        result = await self.db.execute(query)
        notification = result.scalar_one_or_none()
        if notification:
            notification.is_read = True
            await self.db.commit()

    # --- DELIVERIES ---
    async def assign_delivery(self, order_id: UUID, agent_id: UUID) -> Delivery:
        delivery = Delivery(
            order_id=order_id,
            agent_id=agent_id,
            tracking_number=f"TRK-{uuid.uuid4().hex[:8].upper()}"
        )
        self.db.add(delivery)
        await self.db.commit()
        await self.db.refresh(delivery)
        return delivery

    async def update_delivery_status(self, delivery_id: UUID, agent_id: UUID, update_data: DeliveryUpdate):
        query = select(Delivery).where(Delivery.id == delivery_id, Delivery.agent_id == agent_id)
        result = await self.db.execute(query)
        delivery = result.scalar_one_or_none()
        
        if not delivery:
            raise HTTPException(status_code=404, detail="Delivery not found or unassigned")
            
        delivery.status = update_data.status
        if update_data.delivery_notes:
            delivery.delivery_notes = update_data.delivery_notes
            
        await self.db.commit()
        await self.db.refresh(delivery)
        return delivery
