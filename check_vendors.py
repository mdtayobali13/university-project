import asyncio
import sys
import os
sys.path.append(os.path.abspath("."))
from app.core.database import AsyncSessionLocal
from app.models.vendor import Vendor
from sqlalchemy import select

async def run():
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Vendor))
        vendors = result.scalars().all()
        for v in vendors:
            print(f"Store: {v.store_name}, Status: {v.status}")

if __name__ == "__main__":
    asyncio.run(run())
