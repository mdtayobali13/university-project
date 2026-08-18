from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.vendor import Vendor
from app.schemas.vendor import VendorCreate, VendorUpdate
from fastapi import HTTPException
from uuid import UUID

class VendorService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_vendor(self, user_id: UUID, vendor_in: VendorCreate) -> Vendor:
        query = select(Vendor).where(Vendor.user_id == user_id)
        result = await self.db.execute(query)
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="User already has a vendor profile")
            
        vendor = Vendor(
            user_id=user_id,
            **vendor_in.model_dump()
        )
        self.db.add(vendor)
        await self.db.commit()
        await self.db.refresh(vendor)
        return vendor

    async def get_all_vendors(self):
        query = select(Vendor)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_vendor_by_id(self, vendor_id: UUID) -> Vendor:
        query = select(Vendor).where(Vendor.id == vendor_id)
        result = await self.db.execute(query)
        vendor = result.scalar_one_or_none()
        if not vendor:
            raise HTTPException(status_code=404, detail="Vendor not found")
        return vendor

    async def update_vendor(self, vendor_id: UUID, vendor_in: VendorUpdate) -> Vendor:
        vendor = await self.get_vendor_by_id(vendor_id)
        update_data = vendor_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(vendor, field, value)
        await self.db.commit()
        await self.db.refresh(vendor)
        return vendor

    async def delete_vendor(self, vendor_id: UUID):
        vendor = await self.get_vendor_by_id(vendor_id)
        await self.db.delete(vendor)
        await self.db.commit()
        return True
