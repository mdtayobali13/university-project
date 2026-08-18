from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List
from app.core.database import get_db
from app.schemas.address import AddressCreate, AddressUpdate, AddressResponse
from app.schemas.common import StandardResponse
from app.services.address_service import AddressService
from app.api.deps import get_current_active_user
from app.models.user import User, UserRole

router = APIRouter()

def check_user_authorization(user_id: UUID, current_user: User):
    if current_user.id != user_id and current_user.role not in [UserRole.ADMIN, UserRole.SUPER_ADMIN]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this user's addresses")

@router.get("/{user_id}", response_model=StandardResponse[List[AddressResponse]])
async def get_addresses(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    check_user_authorization(user_id, current_user)
    address_service = AddressService(db)
    addresses = await address_service.get_user_addresses(user_id)
    return StandardResponse(success=True, message="Addresses retrieved", data=addresses)

@router.post("/{user_id}", response_model=StandardResponse[AddressResponse])
async def create_address(
    user_id: UUID,
    address_in: AddressCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    check_user_authorization(user_id, current_user)
    address_service = AddressService(db)
    address = await address_service.create_address(user_id, address_in)
    return StandardResponse(success=True, message="Address created", data=address)

@router.patch("/{user_id}/{address_id}", response_model=StandardResponse[AddressResponse])
async def update_address(
    user_id: UUID,
    address_id: UUID,
    address_in: AddressUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    check_user_authorization(user_id, current_user)
    address_service = AddressService(db)
    address = await address_service.update_address(user_id, address_id, address_in)
    return StandardResponse(success=True, message="Address updated", data=address)

@router.delete("/{user_id}/{address_id}", response_model=StandardResponse[None])
async def delete_address(
    user_id: UUID,
    address_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    check_user_authorization(user_id, current_user)
    address_service = AddressService(db)
    await address_service.delete_address(user_id, address_id)
    return StandardResponse(success=True, message="Address deleted", data=None)

