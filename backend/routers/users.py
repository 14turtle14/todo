from typing import List
from fastapi import APIRouter, HTTPException, Depends

from database.database import get_db
from models.schemas.user_schema import UserResponse
from services import user_service
from sqlalchemy.ext.asyncio import AsyncSession

from services.auth_service import get_current_user

router = APIRouter(
    prefix="/users",  
    tags=["Users"], 
)

@router.get("/me", response_model=UserResponse)
async def read_user(user_id: int = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    user = await user_service.find_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/", response_model=List[UserResponse])
async def get_users(db: AsyncSession = Depends(get_db)):
    user_list = await user_service.get_users(db)
    if not user_list:
        raise HTTPException(status_code=404, detail="User not found")
    return user_list

@router.delete("/me", response_model=UserResponse)
async def delete_user(user_id: int = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    user = await user_service.delete_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
    