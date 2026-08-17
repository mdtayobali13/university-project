from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
from app.schemas.category import CategoryCreate, CategoryResponse
from app.schemas.common import StandardResponse
from app.services.category_service import CategoryService

router = APIRouter()

@router.post("/", response_model=StandardResponse[CategoryResponse])
async def create_category(category_in: CategoryCreate, db: AsyncSession = Depends(get_db)):
    category_service = CategoryService(db)
    category = await category_service.create_category(category_in)
    return StandardResponse(success=True, message="Category created", data=category)

@router.get("/", response_model=StandardResponse[List[CategoryResponse]])
async def get_categories(db: AsyncSession = Depends(get_db)):
    category_service = CategoryService(db)
    categories = await category_service.get_all_categories()
    return StandardResponse(success=True, message="Categories retrieved", data=categories)
