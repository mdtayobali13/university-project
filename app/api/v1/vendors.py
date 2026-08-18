from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID
from app.core.database import get_db
from app.schemas.vendor import VendorCreate, VendorUpdate, VendorResponse
from app.schemas.common import StandardResponse
from app.services.vendor_service import VendorService
from app.api.deps import get_current_active_user
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=StandardResponse[List[VendorResponse]])
async def get_all_vendors(db: AsyncSession = Depends(get_db)):
    vendor_service = VendorService(db)
    vendors = await vendor_service.get_all_vendors()
    return StandardResponse(success=True, message="Vendors retrieved successfully", data=vendors)


@router.post("/", response_model=StandardResponse[VendorResponse])
async def create_vendor(
    vendor_in: VendorCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    vendor_service = VendorService(db)
    vendor = await vendor_service.create_vendor(current_user.id, vendor_in)
    return StandardResponse(success=True, message="Vendor created successfully", data=vendor)

@router.get("/{vendor_id}", response_model=StandardResponse[VendorResponse])
async def get_vendor(vendor_id: UUID, db: AsyncSession = Depends(get_db)):
    vendor_service = VendorService(db)
    vendor = await vendor_service.get_vendor_by_id(vendor_id)
    return StandardResponse(success=True, message="Vendor retrieved successfully", data=vendor)

@router.patch("/{vendor_id}", response_model=StandardResponse[VendorResponse])
async def update_vendor(
    vendor_id: UUID,
    vendor_in: VendorUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    vendor_service = VendorService(db)
    vendor = await vendor_service.update_vendor(vendor_id, vendor_in)
    return StandardResponse(success=True, message="Vendor updated successfully", data=vendor)

@router.delete("/{vendor_id}", response_model=StandardResponse[None])
async def delete_vendor(
    vendor_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    vendor_service = VendorService(db)
    await vendor_service.delete_vendor(vendor_id)
    return StandardResponse(success=True, message="Vendor deleted successfully", data=None)

