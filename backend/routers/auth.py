from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr

from backend.database.database import get_db
from backend.services.auth_service import change_user_password, create_access_token, get_current_user, get_password_hash, verify_password
from backend.services.user_service import create_user, get_user_by_email, get_user_by_login, get_user_by_username, update_user_email, update_user_username
from backend.models.schemas.user_schema import Token, UserCreate, UserLogin, UserResponse
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(
    prefix="/auth", 
    tags=["Auth"],
)

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

@router.post("/token", response_model=Token)
async def login(user: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    db_user = await get_user_by_login(db, user.username)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    elif not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Incorrect username/email or password")
    
    access_token = create_access_token(data={"sub": str(db_user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
async def logout(user_id: int = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    pass # refresh

@router.post("/change/password", response_model=UserResponse)
async def change_password(password_old: str, password_new: str, user_id: int = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await change_user_password(password_old, password_new, user_id, db)

@router.post("/change/username", response_model=UserResponse)
async def change_username(username: str, user_id: int = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await update_user_username(db, username_new=username, user_id=user_id)

@router.post("/change/email", response_model=UserResponse)
async def change_email(email: EmailStr, user_id: int = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await update_user_email(db, email_new=email, user_id=user_id)