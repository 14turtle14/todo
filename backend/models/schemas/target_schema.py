from pydantic import BaseModel, ConfigDict, field_validator
from typing import List, Optional

from models.schemas.task_schema import TaskResponse

class TargetBase(BaseModel):
    title: str

    @field_validator("title")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Name must not be empty")
        return value.strip()

class TargetCreate(TargetBase):
    pass

class TargetResponse(TargetBase):
    id: int
    user_id: int
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
    title: Optional[str]