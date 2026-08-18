from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.address import Address
from app.schemas.address import AddressCreate, AddressUpdate
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

    async def get_address(self, user_id: UUID, address_id: UUID) -> Address:
        query = select(Address).where(Address.id == address_id, Address.user_id == user_id)
        result = await self.db.execute(query)
        address = result.scalar_one_or_none()
        if not address:
            raise HTTPException(status_code=404, detail="Address not found")
        return address

    async def update_address(self, user_id: UUID, address_id: UUID, address_in: AddressUpdate) -> Address:
        address = await self.get_address(user_id, address_id)
        update_data = address_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(address, field, value)
        await self.db.commit()
        await self.db.refresh(address)
        return address

    async def delete_address(self, user_id: UUID, address_id: UUID):
        address = await self.get_address(user_id, address_id)
        await self.db.delete(address)
        await self.db.commit()
        return True
