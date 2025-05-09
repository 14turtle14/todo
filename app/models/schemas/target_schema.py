from pydantic import BaseModel
from typing import List, Optional

from app.models.schemas.task_schema import TaskResponse

class TargetBase(BaseModel):
    name: str
    deadline: int
    is_done: bool

class TargetCreate(TargetBase):
    pass

class TargetResponse(TargetBase):
    id: int
    owner_id: int
    tasks: List["TaskResponse"]

    class Config:
        orm_mode = True

class TargetUpdate(BaseModel):
    name: Optional[str]
    deadline: Optional[str]
    is_done: Optional[bool]