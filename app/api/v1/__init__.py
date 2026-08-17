from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.vendors import router as vendors_router
from app.api.v1.categories import router as categories_router
from app.api.v1.products import router as products_router
from app.api.v1.cart import router as cart_router
from app.api.v1.wishlist import router as wishlist_router
from app.api.v1.addresses import router as addresses_router
from app.api.v1.coupons import router as coupons_router
from app.api.v1.orders import router as orders_router
from app.api.v1.payments import router as payments_router
from app.api.v1.payouts import router as payouts_router
from app.api.v1.engagement import router as engagement_router
from app.api.v1.admin import router as admin_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(vendors_router, prefix="/vendors", tags=["Vendors"])
api_router.include_router(categories_router, prefix="/categories", tags=["Categories"])
api_router.include_router(products_router, prefix="/products", tags=["Products"])
api_router.include_router(cart_router, prefix="/cart", tags=["Cart"])
api_router.include_router(wishlist_router, prefix="/wishlist", tags=["Wishlist"])
api_router.include_router(addresses_router, prefix="/addresses", tags=["Addresses"])
api_router.include_router(coupons_router, prefix="/coupons", tags=["Coupons"])
api_router.include_router(orders_router, prefix="/orders", tags=["Orders"])
api_router.include_router(payments_router, prefix="/payments", tags=["Payments"])
api_router.include_router(payouts_router, prefix="/payouts", tags=["Payouts"])
api_router.include_router(engagement_router, prefix="/engagement", tags=["Engagement"])
api_router.include_router(admin_router, prefix="/admin", tags=["Admin"])
