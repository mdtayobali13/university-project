import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.core.config import settings
from app.models.base import BaseModel
# Import all models here so Alembic can discover them
from app.models.user import User
from app.models.vendor import Vendor
from app.models.category import Category
from app.models.brand import Brand
from app.models.product import Product, ProductVariation
from app.models.cart import Cart, CartItem
from app.models.wishlist import Wishlist
from app.models.address import Address
from app.models.coupon import Coupon
from app.models.order import Order, VendorOrder, OrderItem, OrderStatusHistory
from app.models.payment import Payment
from app.models.payout import Commission, Payout
from app.models.engagement import Review, Notification, Delivery

config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = BaseModel.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()

def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
