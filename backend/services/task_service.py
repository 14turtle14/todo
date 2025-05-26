from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.models import Task
from backend.models.schemas.task_schema import TaskCreate, TaskUpdate
from sqlalchemy.future import select

from backend.services.target_service import find_target

async def create_task(db: AsyncSession, task: TaskCreate, user_id: int):
    db_target = await find_target(db, task.target_id, user_id)
    if not db_target:
         return None
    db_task = Task(**task.model_dump())
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task

async def find_task(db: AsyncSession, task_id: int, target_id: int, user_id: int):
    db_target = await find_target(db, target_id, user_id)
    if not db_target:
         return None
    db_task = await db.execute(select(Task).where(Task.id == task_id, Task.target_id == target_id))
    return db_task.scalars().first()

async def delete_task(db: AsyncSession, task_id: int, target_id: int, user_id):
    db_target = await find_target(db, target_id, user_id)
    if not db_target:
         return None
    db_task = await find_task(db, task_id, target_id, user_id)
    if not db_task:
         return None
    await db.delete(db_task)
    await db.commit()
    return db_task

async def get_tasks(db: AsyncSession, target_id: int, user_id):
    db_target = await find_target(db, target_id, user_id)
    if not db_target:
         return None
    db_tasks = await db.execute(select(Task).where(Task.target_id == target_id))
    return db_tasks.scalars().all()

async def update_task(db: AsyncSession, task: TaskUpdate, task_id: int, target_id: int, user_id):
    db_target = await find_target(db, target_id, user_id)
    if not db_target:
         return None
    db_task = await find_task(db, task_id, target_id, user_id)
    if not db_task:
         return None
    for field, value in task.model_dump(exclude_unset=True).items():
            setattr(db_task, field, value)
        
    await db.commit()
    await db.refresh(db_task)
    return db_task