from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from app.core.redis_client import redis_client
import time

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int = 100, window: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window = window

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        key = f"rate_limit:{client_ip}"
        
        # Simple rate limiting using Redis
        try:
            current_count = await redis_client.get(key)
            if current_count and int(current_count) > self.max_requests:
                return JSONResponse(
                    status_code=429,
                    content={"detail": "Too many requests. Please try again later."}
                )
            
            if not current_count:
                await redis_client.setex(key, self.window, 1)
            else:
                await redis_client.incr(key)
                
        except Exception as e:
            # If redis is down, fallback to allowing the request
            pass
            
        response = await call_next(request)
        return response
