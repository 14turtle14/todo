from pydantic import BaseModel, EmailStr
from typing import List, Optional, Union

from app.models.schemas.target_schema import TargetResponse

class UserBase(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    login: Union[EmailStr, str]
    password: str

class UserCreate(UserBase):
    pass

class Token(BaseModel):
    access_token: str
    token_type: str

class UserResponse(UserBase):
    id: int
    targets: List["TargetResponse"]  

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]