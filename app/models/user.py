from sqlalchemy import Column, String, Boolean, Enum
from app.models.base import BaseModel
import enum

class UserRole(str, enum.Enum):
    CUSTOMER = "customer"
    VENDOR = "vendor"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"
    DELIVERY_AGENT = "delivery_agent"

class User(BaseModel):
    __tablename__ = "users"
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(UserRole), default=UserRole.CUSTOMER)
