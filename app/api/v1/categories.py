from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID
from app.core.database import get_db
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.schemas.common import StandardResponse
from app.services.category_service import CategoryService
from app.api.deps import get_current_admin
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=StandardResponse[CategoryResponse])
async def create_category(
    category_in: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    category_service = CategoryService(db)
    category = await category_service.create_category(category_in)
    return StandardResponse(success=True, message="Category created", data=category)

@router.get("/", response_model=StandardResponse[List[CategoryResponse]])
async def get_categories(db: AsyncSession = Depends(get_db)):
    category_service = CategoryService(db)
    categories = await category_service.get_all_categories()
    return StandardResponse(success=True, message="Categories retrieved", data=categories)

@router.patch("/{category_id}", response_model=StandardResponse[CategoryResponse])
async def update_category(
    category_id: UUID,
    category_in: CategoryUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    category_service = CategoryService(db)
    category = await category_service.update_category(category_id, category_in)
    return StandardResponse(success=True, message="Category updated", data=category)

@router.delete("/{category_id}", response_model=StandardResponse[None])
async def delete_category(
    category_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    category_service = CategoryService(db)
    await category_service.delete_category(category_id)
    return StandardResponse(success=True, message="Category deleted", data=None)

