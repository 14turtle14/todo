from pydantic import BaseModel
from typing import List, Optional

from app.models.schemas.task_schema import TaskResponse

class TargetBase(BaseModel):
    name: str
    deadline: int
    owner_id: int

class TargetCreate(TargetBase):
    id: int

class TargetResponse(TargetBase):
    id: int
    tasks: List["TaskResponse"]

    class Config:
        orm_mode = True

class TargetUpdate(BaseModel):
    name: Optional[str]
    deadline: Optional[str]