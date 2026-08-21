import asyncio
import sys
import os
sys.path.append(os.path.abspath("."))
from app.core.database import AsyncSessionLocal, engine
from app.models.base import BaseModel
from app.models.user import User, UserRole
from app.models.vendor import Vendor, VendorStatus
from app.models.category import Category
from app.models.product import Product, ProductStatus
from app.core.security import get_password_hash
from sqlalchemy.future import select

async def get_or_create_user(db, email, hashed_password, full_name, role):
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user:
        user = User(email=email, hashed_password=hashed_password, full_name=full_name, role=role)
        db.add(user)
        await db.flush()
    return user

async def seed_data():
    async with AsyncSessionLocal() as db:
        print("Creating users...")
        # Users
        admin_pass = get_password_hash("admin123")
        vendor_pass = get_password_hash("vendor123")
        customer_pass = get_password_hash("customer123")

        admin = await get_or_create_user(db, "admin@versity.com", admin_pass, "System Admin", UserRole.SUPER_ADMIN)
        vendor1_user = await get_or_create_user(db, "techworld@dev.com", vendor_pass, "Tech World Owner", UserRole.VENDOR)
        vendor2_user = await get_or_create_user(db, "fashionbd@dev.com", vendor_pass, "Fashion BD Owner", UserRole.VENDOR)
        customer = await get_or_create_user(db, "customer@versity.com", customer_pass, "Demo Customer", UserRole.CUSTOMER)
        
        print("Creating vendors...")
        # Vendors
        result = await db.execute(select(Vendor).where(Vendor.store_name == "Tech World BD"))
        vendor1 = result.scalar_one_or_none()
        if not vendor1:
            vendor1 = Vendor(
                user_id=vendor1_user.id,
                store_name="Tech World BD",
                owner_name="Tech World Owner",
                email="techworld@dev.com",
                phone="01711111111",
                address="Dhaka, BD",
                status=VendorStatus.APPROVED
            )
            db.add(vendor1)

        result = await db.execute(select(Vendor).where(Vendor.store_name == "Fashion BD"))
        vendor2 = result.scalar_one_or_none()
        if not vendor2:
            vendor2 = Vendor(
                user_id=vendor2_user.id,
                store_name="Fashion BD",
                owner_name="Fashion BD Owner",
                email="fashionbd@dev.com",
                phone="01822222222",
                address="Chittagong, BD",
                status=VendorStatus.APPROVED
            )
            db.add(vendor2)
            
        await db.flush()
        
        print("Creating categories...")
        # Categories
        cat_elec = Category(name="Electronics", slug="electronics", description="Gadgets and devices", is_active=True)
        cat_fash = Category(name="Fashion", slug="fashion", description="Clothing and apparel", is_active=True)
        cat_home = Category(name="Home & Living", slug="home", description="Furniture and decor", is_active=True)
        
        for cat in [cat_elec, cat_fash, cat_home]:
            res = await db.execute(select(Category).where(Category.slug == cat.slug))
            if not res.scalar_one_or_none():
                db.add(cat)
                
        await db.flush()

        print("Creating products...")
        # Products
        products_data = [
            {
                "name": "Apple MacBook Pro M3",
                "slug": "macbook-pro-m3",
                "sku": "MBP-M3-001",
                "description": "Latest Apple MacBook Pro with M3 chip.",
                "short_description": "Powerful laptop for professionals.",
                "price": 250000.00,
                "stock_quantity": 10,
                "category_id": cat_elec.id,
                "vendor_id": vendor1.id,
                "status": ProductStatus.PUBLISHED,
                "images": ["https://placehold.co/400x400?text=MacBook"]
            },
            {
                "name": "Sony WH-1000XM5",
                "slug": "sony-wh-1000xm5",
                "sku": "SNY-WH-005",
                "description": "Industry leading noise canceling headphones.",
                "short_description": "Premium wireless headphones.",
                "price": 35000.00,
                "stock_quantity": 25,
                "category_id": cat_elec.id,
                "vendor_id": vendor1.id,
                "status": ProductStatus.PUBLISHED,
                "images": ["https://placehold.co/400x400?text=Sony+Headphones"]
            },
            {
                "name": "Men's Classic T-Shirt",
                "slug": "mens-classic-tshirt",
                "sku": "TS-M-01",
                "description": "100% cotton classic fit t-shirt.",
                "short_description": "Comfortable everyday wear.",
                "price": 500.00,
                "stock_quantity": 100,
                "category_id": cat_fash.id,
                "vendor_id": vendor2.id,
                "status": ProductStatus.PUBLISHED,
                "images": ["https://placehold.co/400x400?text=T-Shirt"]
            },
            {
                "name": "Women's Summer Dress",
                "slug": "womens-summer-dress",
                "sku": "DR-W-01",
                "description": "Floral pattern summer dress.",
                "short_description": "Perfect for summer days.",
                "price": 1200.00,
                "stock_quantity": 50,
                "category_id": cat_fash.id,
                "vendor_id": vendor2.id,
                "status": ProductStatus.PUBLISHED,
                "images": ["https://placehold.co/400x400?text=Dress"]
            },
            {
                "name": "Modern Coffee Table",
                "slug": "modern-coffee-table",
                "sku": "CT-H-01",
                "description": "Wooden coffee table with glass top.",
                "short_description": "Elegant living room furniture.",
                "price": 4500.00,
                "stock_quantity": 15,
                "category_id": cat_home.id,
                "vendor_id": vendor1.id,
                "status": ProductStatus.PUBLISHED,
                "images": ["https://placehold.co/400x400?text=Coffee+Table"]
            }
        ]

        for p_data in products_data:
            res = await db.execute(select(Product).where(Product.slug == p_data["slug"]))
            if not res.scalar_one_or_none():
                prod = Product(**p_data)
                db.add(prod)

        await db.commit()
        print("Demo data successfully injected!")

async def main():
    print("Creating tables (if not exists)...")
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
    
    await seed_data()

if __name__ == "__main__":
    asyncio.run(main())
