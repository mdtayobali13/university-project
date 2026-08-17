from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.address import Address
from app.schemas.address import AddressCreate
from fastapi import HTTPException
from uuid import UUID

class AddressService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_address(self, user_id: UUID, address_in: AddressCreate) -> Address:
        address = Address(user_id=user_id, **address_in.model_dump())
        self.db.add(address)
        await self.db.commit()
        await self.db.refresh(address)
        return address

    async def get_user_addresses(self, user_id: UUID):
        query = select(Address).where(Address.user_id == user_id)
        result = await self.db.execute(query)
        return result.scalars().all()
