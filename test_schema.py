import asyncio
import sys
import os
sys.path.append(os.path.abspath("."))
from app.schemas.vendor import VendorResponse
from app.models.vendor import VendorStatus
from uuid import uuid4
from datetime import datetime

v = VendorResponse(
    id=uuid4(),
    user_id=uuid4(),
    store_name="Test Store",
    owner_name="Owner",
    email="test@test.com",
    phone="12345",
    address="123",
    status=VendorStatus.PENDING,
    created_at=datetime.utcnow()
)
print("Vendor JSON:")
print(v.model_dump_json())
