from pydantic import BaseModel
from typing import List

class UserBase(BaseModel):
    username: str
    email: str
    password: str

class UserCreate(UserBase):
    id: int

class TaskBase(BaseModel):
    name: str
    deadline: int

class TaskCreate(TaskBase):
    id: int
    target: "TargetResponse"

class TargetBase(BaseModel):
    name: str
    deadline: int
    owner: "UserResponse"

class TargetCreate(UserBase):
    id: int

class UserResponse(UserBase):
    id: int
    targets: List["TargetResponse"]  

    class Config:
        orm_mode = True

class TaskResponse(UserBase):
    id: int 

    class Config:
        orm_mode = True

class TargetResponse(TargetBase):
    id: int
    tasks: List["TaskResponse"]

    class Config:
        orm_mode = True