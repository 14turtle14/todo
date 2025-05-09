from typing import List
from fastapi import APIRouter, HTTPException, Depends

from app.database.database import get_db
from app.models.schemas.target_schema import TargetCreate, TargetResponse, TargetUpdate
from app.services import target_service
from sqlalchemy.orm import AsyncSession
from app.services.auth_service import get_current_user

router = APIRouter(
    prefix="/targets",  
    tags=["Targets"], 
)

@router.post("/", response_model=TargetResponse)
def create_target(target: TargetCreate, user_id: int = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return target_service.create_target(db, target, user_id)

@router.get("/{target_id}", response_model=TargetResponse)
def read_target(target_id: int, user_id: int = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    target = target_service.find_target(db, target_id, user_id)
    if not target:
        raise HTTPException(status_code=404, detail="Target not found")
    return target

@router.get("/", response_model=List[TargetResponse])
def get_targets(user_id: int = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    target_list = target_service.get_targets(db, user_id)
    if not target_list:
        raise HTTPException(status_code=404, detail="Targets not found")
    return target_list

@router.delete("/{target_id}", response_model=TargetResponse)
def delete_target(target_id: int, user_id: int = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    target = target_service.delete_target(db, target_id, user_id)
    if not target:
        raise HTTPException(status_code=404, detail="Target not found")
    return target

@router.patch("/{target_id}", response_model=TargetResponse)
def update_target(target_id: int, target: TargetUpdate, user_id: int = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    target = target_service.update_target(target, target_id, db, user_id)
    if not target:
        raise HTTPException(status_code=404, detail="Target not found")
    return target