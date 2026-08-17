from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password, create_access_token
from fastapi import HTTPException

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_user(self, user_in: UserCreate) -> User:
        query = select(User).where(User.email == user_in.email)
        result = await self.db.execute(query)
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Email already registered")
        
        user = User(
            email=user_in.email,
            hashed_password=get_password_hash(user_in.password),
            full_name=user_in.full_name
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def authenticate(self, email: str, password: str):
        query = select(User).where(User.email == email)
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()
        
        if not user or not verify_password(password, user.hashed_password):
            return None
            
        return create_access_token(subject=user.id)
