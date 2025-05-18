from pydantic import BaseModel, ConfigDict, EmailStr, ValidationInfo, field_validator, model_validator
from typing import List, Optional, Union

from backend.models.schemas.target_schema import TargetResponse

class UserBase(BaseModel):
    username: str
    email: EmailStr
    password: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Username must not be empty")
        return value.strip()

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str, info: ValidationInfo) -> str:
        if not value.strip():
            raise ValueError("Password must not be empty")
        if len(value) < 8:
            raise ValueError("Password must be longer than 8 characters")
        if "username" in info.data and value == info.data["username"]:
            raise ValueError("Password must not match username")
        return value

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
    targets: List["TargetResponse"] = []

    model_config = ConfigDict(
        json_schema_extra = {
        "example": {
            "id": 1,
            "username": "ivan_petrov",
            "email": "ivan@example.com",
            "targets": [
                {
                    "id": 1,
                    "title": "Подготовка к переезду",
                    "deadline": "2023-12-31",
                    "tasks": [
                        {
                            "id": 1,
                            "title": "Упаковать книги",
                            "is_completed": False
                        },
                        {
                            "id": 2,
                            "title": "Заказать грузчиков",
                            "is_completed": True
                        }
                    ]
                },
                {
                    "id": 2,
                    "title": "Здоровье",
                    "deadline": "2023-11-15",
                    "tasks": [
                        {
                            "id": 3,
                            "title": "Записаться к терапевту",
                            "is_completed": False
                        }
                    ]
                }
            ]
        }
    }
    )
        
class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]

    @model_validator(mode="after")
    def check_at_least_one_field(self) -> "UserUpdate":
        if all(field is None for field in [self.username, self.email, self.password]):
            raise ValueError("At least one filed must be updated")
        return self
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, value: Optional[str]) -> Optional[str]:
        if value is not None and len(value) < 8:
            raise ValueError("Password must be longer than 8 characters")
        return value