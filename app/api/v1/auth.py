from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import AuthService
from app.schemas.common import StandardResponse

router = APIRouter()

@router.post("/register", response_model=StandardResponse[UserResponse])
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)
    user = await auth_service.register_user(user_in)
    return StandardResponse(success=True, message="User registered successfully", data=user)

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)
    token_data = await auth_service.authenticate(form_data.username, form_data.password)
    if not token_data:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    return {"access_token": token_data, "token_type": "bearer"}
