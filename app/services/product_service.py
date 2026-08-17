from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.product import Product, ProductVariation
from app.schemas.product import ProductCreate
from fastapi import HTTPException
from uuid import UUID

class ProductService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_product(self, vendor_id: UUID, product_in: ProductCreate) -> Product:
        # separate variations
        product_data = product_in.model_dump(exclude={"variations"})
        variations_data = product_in.variations or []
        
        product = Product(vendor_id=vendor_id, **product_data)
        self.db.add(product)
        await self.db.commit()
        await self.db.refresh(product)
        
        for var in variations_data:
            variation = ProductVariation(product_id=product.id, **var.model_dump())
            self.db.add(variation)
            
        if variations_data:
            await self.db.commit()
            await self.db.refresh(product)
            
        return product

    async def get_product(self, product_id: UUID) -> Product:
        query = select(Product).where(Product.id == product_id)
        result = await self.db.execute(query)
        product = result.scalar_one_or_none()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
