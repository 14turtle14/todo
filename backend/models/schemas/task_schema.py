from typing import Optional
from pydantic import BaseModel, ConfigDict, field_validator

class TaskBase(BaseModel):
    name: str
    deadline: int
    is_done: bool

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Name must not be empty")
        return value.strip()

    @field_validator("deadline")
    @classmethod
    def validate_deadline(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("Deadline must be more than 0")
        return value

class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    id: int
    target_id: int
    user_id: int

    model_config = ConfigDict(
        json_schema_extra = {
        "example": {
            "name": "Купить молоко",
            "deadline": "2 days"
        }
    }
    )
    

class TaskUpdate(BaseModel):
    name: Optional[str]
    deadline: Optional[str]
    is_done: Optional[bool]