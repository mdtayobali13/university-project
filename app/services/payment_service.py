from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.payment import Payment, PaymentStatus
from app.models.order import Order
from fastapi import HTTPException
from uuid import UUID

class BasePaymentGateway:
    async def process_payment(self, payment: Payment, order: Order) -> str:
        raise NotImplementedError
        
    async def verify_webhook(self, payload: dict) -> bool:
        raise NotImplementedError

class StripeGateway(BasePaymentGateway):
    async def process_payment(self, payment: Payment, order: Order) -> str:
        # Mocking stripe session URL generation
        return f"https://checkout.stripe.com/pay/{payment.id}"
        
    async def verify_webhook(self, payload: dict) -> bool:
        # Mocking stripe webhook signature verification
        return True

class SSLCommerzGateway(BasePaymentGateway):
    async def process_payment(self, payment: Payment, order: Order) -> str:
        # Mocking SSLCommerz session URL generation
        return f"https://sandbox.sslcommerz.com/gwprocess/v4/api.php?{payment.id}"
        
    async def verify_webhook(self, payload: dict) -> bool:
        return True

class CODGateway(BasePaymentGateway):
    async def process_payment(self, payment: Payment, order: Order) -> str:
        return "success" # COD is instantly successful to process (no URL)

class PaymentService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.gateways = {
            "stripe": StripeGateway(),
            "sslcommerz": SSLCommerzGateway(),
            "cod": CODGateway()
        }

    async def initiate_payment(self, user_id: UUID, order_id: UUID, gateway_name: str):
        query = select(Order).where(Order.id == order_id, Order.user_id == user_id)
        result = await self.db.execute(query)
        order = result.scalar_one_or_none()
        
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
            
        if gateway_name not in self.gateways:
            raise HTTPException(status_code=400, detail="Invalid payment gateway")
            
        payment = Payment(
            order_id=order.id,
            user_id=user_id,
            amount=order.grand_total,
            gateway=gateway_name
        )
        self.db.add(payment)
        await self.db.flush()
        
        gateway = self.gateways[gateway_name]
        payment_url = await gateway.process_payment(payment, order)
        
        if gateway_name == "cod":
            payment.status = PaymentStatus.PENDING
            order.payment_status = "pending"
        else:
            payment.status = PaymentStatus.PROCESSING
            
        await self.db.commit()
        await self.db.refresh(payment)
        
        return {"payment_url": payment_url, "payment": payment}
        
    async def handle_webhook(self, gateway_name: str, payload: dict):
        pass
