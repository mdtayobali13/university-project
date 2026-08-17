from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.payout import Payout, Commission, PayoutStatus
from app.schemas.payout import PayoutRequest
from fastapi import HTTPException
from uuid import UUID

class PayoutService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_vendor_commissions(self, vendor_id: UUID):
        query = select(Commission).where(Commission.vendor_id == vendor_id)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def request_payout(self, vendor_id: UUID, request: PayoutRequest) -> Payout:
        # Check if they have enough "ready_for_payout" balance
        query = select(Commission).where(
            Commission.vendor_id == vendor_id,
            Commission.status == "ready_for_payout"
        )
        result = await self.db.execute(query)
        commissions = result.scalars().all()
        
        available_balance = sum(float(c.net_earnings) for c in commissions)
        
        if request.amount > available_balance:
            raise HTTPException(status_code=400, detail="Insufficient ready balance for payout")
            
        payout = Payout(
            vendor_id=vendor_id,
            amount=request.amount,
            bank_account_info=request.bank_account_info
        )
        self.db.add(payout)
        
        # Deduct balance by marking commissions as "processing" or linking them
        # Simplified: Just create the payout request
        await self.db.commit()
        await self.db.refresh(payout)
        return payout
