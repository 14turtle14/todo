from pydantic import BaseModel
from typing import List, Optional

from app.models.schemas.target_schema import TargetResponse

class UserBase(BaseModel):
    username: str
    email: str
    password: str

class UserCreate(UserBase):
    id: int

class UserResponse(UserBase):
    id: int
    targets: List["TargetResponse"]  

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[str]
    password: Optional[str]