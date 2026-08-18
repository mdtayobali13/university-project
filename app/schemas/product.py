from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime
from app.models.product import ProductStatus

class ProductVariationBase(BaseModel):
    sku: str
    price: Optional[float] = None
    stock_quantity: int = 0
    attributes: Dict[str, Any]
    image: Optional[str] = None

class ProductVariationCreate(ProductVariationBase):
    pass

class ProductVariationResponse(ProductVariationBase):
    id: UUID
    product_id: UUID
    
    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    name: str
    slug: str
    sku: str
    description: str
    short_description: Optional[str] = None
    price: float = Field(..., gt=0)
    discount_price: Optional[float] = None
    cost_price: Optional[float] = None
    stock_quantity: int = 0
    low_stock_threshold: int = 5
    category_id: UUID
    brand_id: Optional[UUID] = None
    images: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    is_featured: bool = False

class ProductCreate(ProductBase):
    variations: Optional[List[ProductVariationCreate]] = None

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    sku: Optional[str] = None
    description: Optional[str] = None
    short_description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    discount_price: Optional[float] = None
    cost_price: Optional[float] = None
    stock_quantity: Optional[int] = None
    low_stock_threshold: Optional[int] = None
    category_id: Optional[UUID] = None
    brand_id: Optional[UUID] = None
    images: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    is_featured: Optional[bool] = None

class ProductResponse(ProductBase):
    id: UUID
    vendor_id: UUID
    status: ProductStatus
    rating: float
    review_count: int
    created_at: datetime
    variations: List[ProductVariationResponse] = []
    
    class Config:
        from_attributes = True
