from typing import Optional
from pydantic import BaseModel, ConfigDict, field_validator

class TaskBase(BaseModel):
    title: str
    is_done: bool = False
    is_priorityzed: bool = False
    target_id: int

    @field_validator("title")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Name must not be empty")
        return value.strip()

class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    id: int

    model_config = ConfigDict(
        json_schema_extra = {
        "example": {
            "name": "Купить молоко",
            "deadline": "2 days"
        }
    }
    )
    

class TaskUpdate(BaseModel):
    title: Optional[str]
    is_done: Optional[bool]
    is_priorityzed: Optional[bool]