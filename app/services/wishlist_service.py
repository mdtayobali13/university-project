from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.wishlist import Wishlist
from app.schemas.wishlist import WishlistCreate
from fastapi import HTTPException
from uuid import UUID

class WishlistService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_wishlist(self, user_id: UUID):
        query = select(Wishlist).where(Wishlist.user_id == user_id)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def add_to_wishlist(self, user_id: UUID, item_in: WishlistCreate):
        query = select(Wishlist).where(
            Wishlist.user_id == user_id, 
            Wishlist.product_id == item_in.product_id
        )
        result = await self.db.execute(query)
        
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Product already in wishlist")
            
        wishlist_item = Wishlist(user_id=user_id, product_id=item_in.product_id)
        self.db.add(wishlist_item)
        await self.db.commit()
        await self.db.refresh(wishlist_item)
        return wishlist_item

    async def remove_from_wishlist(self, user_id: UUID, product_id: UUID):
        query = select(Wishlist).where(
            Wishlist.user_id == user_id, 
            Wishlist.product_id == product_id
        )
        result = await self.db.execute(query)
        wishlist_item = result.scalar_one_or_none()
        
        if not wishlist_item:
            raise HTTPException(status_code=404, detail="Product not found in wishlist")
            
        await self.db.delete(wishlist_item)
        await self.db.commit()
        return True
