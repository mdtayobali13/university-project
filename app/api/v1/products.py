from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.core.database import get_db
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.schemas.common import StandardResponse
from app.services.product_service import ProductService
from app.api.deps import get_current_active_user
from app.models.user import User

router = APIRouter()

from typing import List, Optional

@router.post("/", response_model=StandardResponse[ProductResponse])
async def create_product(
    product_in: ProductCreate,
    vendor_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    product_service = ProductService(db)
    product = await product_service.create_product(vendor_id, product_in)
    return StandardResponse(success=True, message="Product created successfully", data=product)

@router.get("/", response_model=StandardResponse[List[ProductResponse]])
async def get_products(
    category_id: Optional[UUID] = None,
    vendor_id: Optional[UUID] = None,
    limit: int = 100,
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
):
    product_service = ProductService(db)
    products = await product_service.get_products(category_id=category_id, vendor_id=vendor_id, limit=limit, offset=offset)
    return StandardResponse(success=True, message="Products retrieved successfully", data=products)

@router.get("/{product_id}", response_model=StandardResponse[ProductResponse])
async def get_product(product_id: UUID, db: AsyncSession = Depends(get_db)):
    product_service = ProductService(db)
    product = await product_service.get_product(product_id)
    return StandardResponse(success=True, message="Product retrieved successfully", data=product)

@router.patch("/{product_id}", response_model=StandardResponse[ProductResponse])
async def update_product(
    product_id: UUID,
    product_in: ProductUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    product_service = ProductService(db)
    product = await product_service.update_product(product_id, product_in)
    return StandardResponse(success=True, message="Product updated successfully", data=product)

@router.delete("/{product_id}", response_model=StandardResponse[None])
async def delete_product(
    product_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    product_service = ProductService(db)
    await product_service.delete_product(product_id)
    return StandardResponse(success=True, message="Product deleted successfully", data=None)

