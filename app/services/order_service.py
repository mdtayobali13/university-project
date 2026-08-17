from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.order import Order, VendorOrder, OrderItem, OrderStatusHistory, OrderStatus
from app.models.cart import Cart, CartItem
from app.models.product import Product, ProductVariation
from app.schemas.order import CheckoutRequest
from fastapi import HTTPException
from uuid import UUID
from datetime import datetime

class OrderService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def checkout(self, user_id: UUID, request: CheckoutRequest) -> Order:
        # 1. Get Cart
        cart_query = select(Cart).where(Cart.user_id == user_id)
        cart_result = await self.db.execute(cart_query)
        cart = cart_result.scalar_one_or_none()
        
        if not cart:
            raise HTTPException(status_code=400, detail="Cart is empty")
            
        items_query = select(CartItem).where(CartItem.cart_id == cart.id)
        items_result = await self.db.execute(items_query)
        cart_items = items_result.scalars().all()
        
        if not cart_items:
            raise HTTPException(status_code=400, detail="Cart is empty")
            
        # 2. Process items and group by vendor
        vendor_totals = {} # vendor_id: subtotal
        vendor_items = {}  # vendor_id: [items]
        
        grand_total = 0.0
        
        for item in cart_items:
            product_query = select(Product).where(Product.id == item.product_id)
            prod_res = await self.db.execute(product_query)
            product = prod_res.scalar_one_or_none()
            
            if not product:
                continue
                
            vendor_id = product.vendor_id
            
            # Determine price and validate stock
            price = float(product.price)
            if item.variation_id:
                var_query = select(ProductVariation).where(ProductVariation.id == item.variation_id)
                var_res = await self.db.execute(var_query)
                variation = var_res.scalar_one_or_none()
                if variation and variation.price:
                    price = float(variation.price)
                if variation.stock_quantity < item.quantity:
                    raise HTTPException(status_code=400, detail=f"Not enough stock for {product.name}")
                # Reserve stock (decrement)
                variation.stock_quantity -= item.quantity
            else:
                if product.stock_quantity < item.quantity:
                    raise HTTPException(status_code=400, detail=f"Not enough stock for {product.name}")
                # Reserve stock (decrement)
                product.stock_quantity -= item.quantity
                
            item_total = price * item.quantity
            grand_total += item_total
            
            if vendor_id not in vendor_totals:
                vendor_totals[vendor_id] = 0.0
                vendor_items[vendor_id] = []
                
            vendor_totals[vendor_id] += item_total
            vendor_items[vendor_id].append({
                "product_id": product.id,
                "variation_id": item.variation_id,
                "quantity": item.quantity,
                "price": price
            })
            
        # 3. Create Parent Order
        order = Order(
            user_id=user_id,
            address_id=request.address_id,
            total_amount=grand_total,
            grand_total=grand_total, # For now assuming no tax/shipping logic here
            payment_method=request.payment_method
        )
        self.db.add(order)
        await self.db.flush() # To get order.id
        
        # 4. Create Vendor Orders
        for v_id, total in vendor_totals.items():
            v_order = VendorOrder(
                parent_order_id=order.id,
                vendor_id=v_id,
                subtotal=total,
                total_amount=total
            )
            self.db.add(v_order)
            await self.db.flush()
            
            for v_item in vendor_items[v_id]:
                order_item = OrderItem(
                    vendor_order_id=v_order.id,
                    **v_item
                )
                self.db.add(order_item)
                
        # 5. Clear Cart
        for item in cart_items:
            await self.db.delete(item)
            
        # 6. Commit transaction
        await self.db.commit()
        await self.db.refresh(order)
        
        return order
        
    async def get_user_orders(self, user_id: UUID):
        query = select(Order).where(Order.user_id == user_id)
        result = await self.db.execute(query)
        return result.scalars().all()
