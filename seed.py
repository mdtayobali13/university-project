import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal, engine
from app.models.base import BaseModel
from app.models.user import User, UserRole
from app.core.security import get_password_hash

async def seed_data():
    async with AsyncSessionLocal() as db:
        # Create super admin
        super_admin = User(
            email="admin@versity.com",
            hashed_password=get_password_hash("admin123"),
            full_name="System Admin",
            role=UserRole.SUPER_ADMIN
        )
        db.add(super_admin)
        
        # Create a demo customer
        customer = User(
            email="customer@versity.com",
            hashed_password=get_password_hash("customer123"),
            full_name="Demo Customer",
            role=UserRole.CUSTOMER
        )
        db.add(customer)
        
        await db.commit()
        print("Seed data successfully injected!")

async def main():
    print("Creating tables...")
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
    print("Tables created.")
    
    await seed_data()

if __name__ == "__main__":
    asyncio.run(main())
