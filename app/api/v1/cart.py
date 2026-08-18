from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.core.database import get_db
from app.schemas.cart import CartResponse, CartItemCreate, CartItemUpdate
from app.schemas.common import StandardResponse
from app.services.cart_service import CartService
from app.api.deps import get_current_active_user
from app.models.user import User, UserRole

router = APIRouter()

def check_user_authorization(user_id: UUID, current_user: User):
    if current_user.id != user_id and current_user.role not in [UserRole.ADMIN, UserRole.SUPER_ADMIN]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this user's cart")

@router.get("/{user_id}", response_model=StandardResponse[CartResponse])
async def get_cart(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    check_user_authorization(user_id, current_user)
    cart_service = CartService(db)
    cart = await cart_service.get_cart(user_id)
    return StandardResponse(success=True, message="Cart retrieved", data=cart)

@router.post("/{user_id}/items", response_model=StandardResponse[CartResponse])
async def add_cart_item(
    user_id: UUID,
    item_in: CartItemCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    check_user_authorization(user_id, current_user)
    cart_service = CartService(db)
    cart = await cart_service.add_item(user_id, item_in)
    return StandardResponse(success=True, message="Item added to cart", data=cart)

@router.patch("/{user_id}/items/{item_id}", response_model=StandardResponse[CartResponse])
async def update_cart_item(
    user_id: UUID,
    item_id: UUID,
    item_in: CartItemUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    check_user_authorization(user_id, current_user)
    cart_service = CartService(db)
    cart = await cart_service.update_item(user_id, item_id, item_in)
    return StandardResponse(success=True, message="Cart item updated", data=cart)

@router.delete("/{user_id}/items/{item_id}", response_model=StandardResponse[CartResponse])
async def remove_cart_item(
    user_id: UUID,
    item_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    check_user_authorization(user_id, current_user)
    cart_service = CartService(db)
    cart = await cart_service.remove_item(user_id, item_id)
    return StandardResponse(success=True, message="Item removed from cart", data=cart)

