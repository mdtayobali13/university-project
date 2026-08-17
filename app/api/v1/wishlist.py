from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List
from app.core.database import get_db
from app.schemas.wishlist import WishlistCreate, WishlistResponse
from app.schemas.common import StandardResponse
from app.services.wishlist_service import WishlistService

router = APIRouter()

@router.get("/{user_id}", response_model=StandardResponse[List[WishlistResponse]])
async def get_wishlist(user_id: UUID, db: AsyncSession = Depends(get_db)):
    wishlist_service = WishlistService(db)
    wishlist = await wishlist_service.get_wishlist(user_id)
    return StandardResponse(success=True, message="Wishlist retrieved", data=wishlist)

@router.post("/{user_id}", response_model=StandardResponse[WishlistResponse])
async def add_to_wishlist(user_id: UUID, item_in: WishlistCreate, db: AsyncSession = Depends(get_db)):
    wishlist_service = WishlistService(db)
    wishlist = await wishlist_service.add_to_wishlist(user_id, item_in)
    return StandardResponse(success=True, message="Added to wishlist", data=wishlist)
