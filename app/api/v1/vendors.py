from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.core.database import get_db
from app.schemas.vendor import VendorCreate, VendorResponse
from app.schemas.common import StandardResponse
from app.services.vendor_service import VendorService

router = APIRouter()

@router.post("/", response_model=StandardResponse[VendorResponse])
async def create_vendor(
    vendor_in: VendorCreate,
    user_id: UUID, 
    db: AsyncSession = Depends(get_db)
):
    vendor_service = VendorService(db)
    vendor = await vendor_service.create_vendor(user_id, vendor_in)
    return StandardResponse(success=True, message="Vendor created successfully", data=vendor)

@router.get("/{vendor_id}", response_model=StandardResponse[VendorResponse])
async def get_vendor(vendor_id: UUID, db: AsyncSession = Depends(get_db)):
    vendor_service = VendorService(db)
    vendor = await vendor_service.get_vendor_by_id(vendor_id)
    return StandardResponse(success=True, message="Vendor retrieved successfully", data=vendor)
