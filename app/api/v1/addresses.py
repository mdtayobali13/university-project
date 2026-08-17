from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List
from app.core.database import get_db
from app.schemas.address import AddressCreate, AddressResponse
from app.schemas.common import StandardResponse
from app.services.address_service import AddressService

router = APIRouter()

@router.get("/{user_id}", response_model=StandardResponse[List[AddressResponse]])
async def get_addresses(user_id: UUID, db: AsyncSession = Depends(get_db)):
    address_service = AddressService(db)
    addresses = await address_service.get_user_addresses(user_id)
    return StandardResponse(success=True, message="Addresses retrieved", data=addresses)

@router.post("/{user_id}", response_model=StandardResponse[AddressResponse])
async def create_address(user_id: UUID, address_in: AddressCreate, db: AsyncSession = Depends(get_db)):
    address_service = AddressService(db)
    address = await address_service.create_address(user_id, address_in)
    return StandardResponse(success=True, message="Address created", data=address)
