from typing import List
from fastapi import APIRouter, HTTPException, Depends

from app.database.database import get_db
from sqlalchemy.orm import AsyncSession
from app.models.schemas.task_schema import TaskCreate, TaskResponse, TaskUpdate
from app.services import task_service
from app.services.auth_service import get_current_user

router = APIRouter(
    prefix="/tasks",  
    tags=["Tasks"], 
)

@router.post("/", response_model=TaskResponse)
async def create_task(task: TaskCreate, target_id: int, db: AsyncSession = Depends(get_db), user_id: int = Depends(get_current_user)):
    return await task_service.create_task(db, task, target_id, user_id)

@router.get("/{task_id}", response_model=TaskResponse)
async def read_task(task_id: int, target_id: int, db: AsyncSession = Depends(get_db), user_id: int = Depends(get_current_user)):
    task = await task_service.find_task(db, task_id, target_id, user_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.get("/", response_model=List[TaskResponse])
async def get_tasks(target_id: int, db: AsyncSession = Depends(get_db), user_id: int = Depends(get_current_user)):
    task_list = await task_service.get_tasks(db, target_id, user_id)
    if not task_list:
        raise HTTPException(status_code=404, detail="Task not found")
    return task_list

@router.delete("/{task_id}", response_model=TaskResponse)
async def delete_task(target_id: int, task_id: int, db: AsyncSession = Depends(get_db), user_id: int = Depends(get_current_user)):
    task = await task_service.delete_task(db, task_id, target_id, user_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(target_id: int, task_id: int, task: TaskUpdate, db: AsyncSession = Depends(get_db), user_id: int = Depends(get_current_user)):
    task = await task_service.update_task(task_id, task, db, target_id, user_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task