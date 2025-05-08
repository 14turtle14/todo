from sqlalchemy.orm import Session

from app.models.schemas.task_schema import TaskCreate, TaskUpdate
from app.models.schemas.user_schema import UserCreate, UserUpdate
from . import models

def create_task(db: Session, task: TaskCreate):
    db_task = models.Task(**task)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def find_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def delete_task(db: Session, task_id: int):
    db_task = find_task(db, task_id)
    db.delete(db_task)
    db.commit()
    db.refresh()
    return db_task

def get_tasks(db: Session):
    return db.query(models.Task).all()

def update_task(db: Session, task: TaskUpdate, task_id: int):
    db_task = find_task(db, task_id)
    for field, value in task.model_dump().items():
            setattr(db_task, field, value)
        
    db.commit()
    db.refresh(db_task)
    return db_task