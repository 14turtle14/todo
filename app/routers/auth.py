from fastapi import APIRouter, Depends, HTTPException

from app.database.database import get_db
from app.services.auth_service import get_password_hash
from app.services.user_service import create_user, get_user_by_email, get_user_by_login, get_user_by_username
from app.models.schemas.user_schema import Token, UserCreate, UserLogin
from sqlalchemy.orm import AsyncSession
from .auth import verify_password, create_access_token


router = APIRouter(prefix="/auth")

@router.post("/signup", response_model=Token)
async def signup(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = await get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = get_password_hash(user.password)
    user.password = hashed_password
    
    new_user = await create_user(db, user)
    
    access_token = create_access_token(data={"sub": str(new_user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    db_user = await get_user_by_login(db, user.login)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username/email or password")
    
    access_token = create_access_token(data={"sub": str(db_user.id)})
    return {"access_token": access_token, "token_type": "bearer"}