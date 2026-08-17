from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.category import Category
from app.schemas.category import CategoryCreate
from fastapi import HTTPException
from uuid import UUID

class CategoryService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_category(self, category_in: CategoryCreate) -> Category:
        query = select(Category).where(Category.name == category_in.name)
        result = await self.db.execute(query)
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Category already exists")
            
        category = Category(**category_in.model_dump())
        self.db.add(category)
        await self.db.commit()
        await self.db.refresh(category)
        return category

    async def get_all_categories(self):
        query = select(Category)
        result = await self.db.execute(query)
        return result.scalars().all()
