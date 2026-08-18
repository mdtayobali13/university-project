from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate
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

    async def get_category(self, category_id: UUID) -> Category:
        query = select(Category).where(Category.id == category_id)
        result = await self.db.execute(query)
        category = result.scalar_one_or_none()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return category

    async def update_category(self, category_id: UUID, category_in: CategoryUpdate) -> Category:
        category = await self.get_category(category_id)
        update_data = category_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(category, field, value)
        await self.db.commit()
        await self.db.refresh(category)
        return category

    async def delete_category(self, category_id: UUID):
        category = await self.get_category(category_id)
        await self.db.delete(category)
        await self.db.commit()
        return True
