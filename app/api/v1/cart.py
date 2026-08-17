from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.core.database import get_db
from app.schemas.cart import CartResponse, CartItemCreate
from app.schemas.common import StandardResponse
from app.services.cart_service import CartService

router = APIRouter()

@router.get("/{user_id}", response_model=StandardResponse[CartResponse])
async def get_cart(user_id: UUID, db: AsyncSession = Depends(get_db)):
    cart_service = CartService(db)
    cart = await cart_service.get_cart(user_id)
    return StandardResponse(success=True, message="Cart retrieved", data=cart)

@router.post("/{user_id}/items", response_model=StandardResponse[CartResponse])
async def add_cart_item(user_id: UUID, item_in: CartItemCreate, db: AsyncSession = Depends(get_db)):
    cart_service = CartService(db)
    cart = await cart_service.add_item(user_id, item_in)
    return StandardResponse(success=True, message="Item added to cart", data=cart)
