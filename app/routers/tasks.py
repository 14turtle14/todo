from typing import List
from fastapi import APIRouter, HTTPException, Depends

from app.database import get_db
from app.models.schemas.user_schema import UserCreate, UserResponse, UserUpdate
from app.services import user_service
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",  
    tags=["Users"], 
)

@router.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, user)

@router.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = user_service.find_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/users/", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    user_list = user_service.get_users(db)
    if not user_list:
        raise HTTPException(status_code=404, detail="User not found")
    return user_list

@router.post("/users/{user_id}", response_model=UserResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = user_service.delete_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    user = user_service.update_user(user_id, user, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user