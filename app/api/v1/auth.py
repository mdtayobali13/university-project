from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Any

from app.core.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import AuthService
from app.schemas.common import StandardResponse
from app.schemas.token import Token
from app.api.deps import get_current_active_user
from app.models.user import User

router = APIRouter()

@router.post("/register", response_model=StandardResponse[UserResponse], status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)) -> Any:
    """
    Register a new user.
    """
    auth_service = AuthService(db)
    user = await auth_service.register_user(user_in)
    return StandardResponse(success=True, message="User registered successfully", data=user)

@router.post("/login", response_model=Token)
async def login(
    db: AsyncSession = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    auth_service = AuthService(db)
    token_data = await auth_service.authenticate(form_data.username, form_data.password)
    if not token_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")
    return {
        "access_token": token_data["access_token"], 
        "refresh_token": token_data["refresh_token"],
        "token_type": "bearer"
    }

from app.schemas.token import RefreshRequest
from app.core.security import create_access_token, create_refresh_token
from app.core.config import settings
from jose import jwt, JWTError

@router.post("/refresh", response_model=Token)
async def refresh_access_token(
    request: RefreshRequest,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Refresh access token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(request.refresh_token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        token_type: str = payload.get("type")
        if user_id is None or token_type != "refresh":
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    # Check if user exists
    user_query = select(User).where(User.id == user_id)
    result = await db.execute(user_query)
    user = result.scalar_one_or_none()
    if not user:
        raise credentials_exception
        
    access_token = create_access_token(subject=user.id)
    refresh_token = create_refresh_token(subject=user.id) # Optional: rotate refresh token
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.get("/me", response_model=StandardResponse[UserResponse])
async def read_users_me(
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return StandardResponse(success=True, message="Current user retrieved", data=current_user)
