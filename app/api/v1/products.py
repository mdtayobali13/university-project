from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.core.database import get_db
from app.schemas.product import ProductCreate, ProductResponse
from app.schemas.common import StandardResponse
from app.services.product_service import ProductService

router = APIRouter()

@router.post("/", response_model=StandardResponse[ProductResponse])
async def create_product(
    product_in: ProductCreate,
    vendor_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    product_service = ProductService(db)
    product = await product_service.create_product(vendor_id, product_in)
    return StandardResponse(success=True, message="Product created successfully", data=product)

@router.get("/{product_id}", response_model=StandardResponse[ProductResponse])
async def get_product(product_id: UUID, db: AsyncSession = Depends(get_db)):
    product_service = ProductService(db)
    product = await product_service.get_product(product_id)
    return StandardResponse(success=True, message="Product retrieved successfully", data=product)
