from sqlalchemy.orm import AsyncSession
from app.models.models import Task
from app.models.schemas.task_schema import TaskCreate, TaskUpdate
from sqlalchemy.future import select

async def create_task(db: AsyncSession, task: TaskCreate, target_id: int, user_id: int):
    db_task = Task(**task, target_id=target_id)
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task

async def find_task(db: AsyncSession, task_id: int, target_id: int, user_id: int):
    return await db.execute(select(Task).where(Task.id == task_id and Task.target_id == target_id)).scalars().first()

async def delete_task(db: AsyncSession, task_id: int, target_id: int, user_id: int):
    db_task = await find_task(db, task_id, target_id, user_id)
    db.delete(db_task)
    await db.commit()
    await db.refresh()
    return db_task

async def get_tasks(db: AsyncSession, target_id: int, user_id: int):
    return await db.execute(select(Task).where(Task.target_id == target_id)).scalars().all()

async def update_task(db: AsyncSession, task: TaskUpdate, task_id: int, target_id: int, user_id: int):
    db_task = await find_task(db, task_id, target_id, user_id)
    for field, value in task.model_dump(exclude_unset=True).items():
            setattr(db_task, field, value)
        
    await db.commit()
    await db.refresh(db_task)
    return db_task