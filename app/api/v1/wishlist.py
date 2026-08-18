from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List
from app.core.database import get_db
from app.schemas.wishlist import WishlistCreate, WishlistResponse
from app.schemas.common import StandardResponse
from app.services.wishlist_service import WishlistService
from app.api.deps import get_current_active_user
from app.models.user import User, UserRole

router = APIRouter()

def check_user_authorization(user_id: UUID, current_user: User):
    if current_user.id != user_id and current_user.role not in [UserRole.ADMIN, UserRole.SUPER_ADMIN]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this user's wishlist")

@router.get("/{user_id}", response_model=StandardResponse[List[WishlistResponse]])
async def get_wishlist(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    check_user_authorization(user_id, current_user)
    wishlist_service = WishlistService(db)
    wishlist = await wishlist_service.get_wishlist(user_id)
    return StandardResponse(success=True, message="Wishlist retrieved", data=wishlist)

@router.post("/{user_id}", response_model=StandardResponse[WishlistResponse])
async def add_to_wishlist(
    user_id: UUID,
    item_in: WishlistCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    check_user_authorization(user_id, current_user)
    wishlist_service = WishlistService(db)
    wishlist = await wishlist_service.add_to_wishlist(user_id, item_in)
    return StandardResponse(success=True, message="Added to wishlist", data=wishlist)

@router.delete("/{user_id}/{product_id}", response_model=StandardResponse[None])
async def remove_from_wishlist(
    user_id: UUID,
    product_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    check_user_authorization(user_id, current_user)
    wishlist_service = WishlistService(db)
    await wishlist_service.remove_from_wishlist(user_id, product_id)
    return StandardResponse(success=True, message="Removed from wishlist", data=None)

