from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.cart import Cart, CartItem
from app.schemas.cart import CartItemCreate, CartItemUpdate
from fastapi import HTTPException
from uuid import UUID

class CartService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_cart(self, user_id: UUID) -> Cart:
        query = select(Cart).where(Cart.user_id == user_id)
        result = await self.db.execute(query)
        cart = result.scalar_one_or_none()
        
        if not cart:
            cart = Cart(user_id=user_id)
            self.db.add(cart)
            await self.db.commit()
            await self.db.refresh(cart)
            
        return cart

    async def add_item(self, user_id: UUID, item_in: CartItemCreate) -> Cart:
        cart = await self.get_cart(user_id)
        
        query = select(CartItem).where(
            CartItem.cart_id == cart.id,
            CartItem.product_id == item_in.product_id,
            CartItem.variation_id == item_in.variation_id
        )
        result = await self.db.execute(query)
        existing_item = result.scalar_one_or_none()
        
        if existing_item:
            existing_item.quantity += item_in.quantity
        else:
            new_item = CartItem(
                cart_id=cart.id,
                **item_in.model_dump()
            )
            self.db.add(new_item)
            
        await self.db.commit()
        return await self.get_cart(user_id)
