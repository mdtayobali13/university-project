from fastapi import FastAPI
from app.core.config import settings
from app.api.v1 import api_router
from app.middleware.rate_limit import RateLimitMiddleware

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.add_middleware(RateLimitMiddleware, max_requests=100, window=60)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {"message": "Welcome to the Multi-Vendor E-commerce API"}
