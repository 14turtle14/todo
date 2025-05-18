from pydantic import BaseModel, ConfigDict, field_validator
from typing import List, Optional

from backend.models.schemas.task_schema import TaskResponse

class TargetBase(BaseModel):
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

class TargetCreate(TargetBase):
    pass

class TargetResponse(TargetBase):
    id: int
    owner_id: int
    tasks: List["TaskResponse"] = []

    model_config = ConfigDict(
        json_schema_extra = {
            "example": {
                "name": "Купить молоко",
                "deadline": "2 days"
            }
        }
    )

class TargetUpdate(BaseModel):
    name: Optional[str]
    deadline: Optional[str]
    is_done: Optional[bool]