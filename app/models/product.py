from sqlalchemy import Column, String, Text, Numeric, Integer, Boolean, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
import enum

class ProductStatus(str, enum.Enum):
    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    PUBLISHED = "published"
    SUSPENDED = "suspended"

class Product(BaseModel):
    __tablename__ = "products"
    
    name = Column(String, index=True, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    sku = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=False)
    short_description = Column(String, nullable=True)
    
    price = Column(Numeric(10, 2), nullable=False)
    discount_price = Column(Numeric(10, 2), nullable=True)
    cost_price = Column(Numeric(10, 2), nullable=True)
    
    stock_quantity = Column(Integer, default=0)
    low_stock_threshold = Column(Integer, default=5)
    
    category_id = Column(ForeignKey("categories.id"), nullable=False)
    brand_id = Column(ForeignKey("brands.id"), nullable=True)
    vendor_id = Column(ForeignKey("vendors.id"), nullable=False)
    
    images = Column(JSON, nullable=True) # list of image urls
    tags = Column(JSON, nullable=True) # list of tags
    
    status = Column(Enum(ProductStatus), default=ProductStatus.DRAFT)
    is_featured = Column(Boolean, default=False)
    
    rating = Column(Numeric(3, 2), default=0.0)
    review_count = Column(Integer, default=0)
    
    category = relationship("Category", back_populates="products")
    brand = relationship("Brand", back_populates="products")
    vendor = relationship("Vendor", back_populates="products")
    variations = relationship("ProductVariation", back_populates="product", cascade="all, delete-orphan")

class ProductVariation(BaseModel):
    __tablename__ = "product_variations"
    
    product_id = Column(ForeignKey("products.id"), nullable=False)
    sku = Column(String, unique=True, index=True, nullable=False)
    price = Column(Numeric(10, 2), nullable=True) # overrides product price if set
    stock_quantity = Column(Integer, default=0)
    attributes = Column(JSON, nullable=False) # e.g. {"size": "M", "color": "Red"}
    image = Column(String, nullable=True)
    
    product = relationship("Product", back_populates="variations")
