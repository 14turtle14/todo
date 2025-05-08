from typing import Optional
from pydantic import BaseModel

from app.models.schemas.target_schema import TargetResponse

class TaskBase(BaseModel):
    name: str
    deadline: int
    target_id: int

class TaskCreate(TaskBase):
    id: int

class TaskResponse(TaskBase):
    id: int 

    class Config:
        orm_mode = True

class TaskUpdate(BaseModel):
    name: Optional[str]
    deadline: Optional[str]