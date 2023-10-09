from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class TaskRequest(BaseModel):
    guest_id: int = Field(..., description="The ID of the associated guest")
    serial: int = Field(0, description="Used to sort the tasks")
    date_time: str = Field(None, description="The date and time for the task")
    name: str = Field(..., description="The name of the task")
    details: str = Field(None, description="Additional details about the task")

    class Config:
        orm_mode = True


class TaskUpdateRequest(BaseModel):
    id: int = Field(..., description="The ID of the Task")
    serial: int = Field(0, description="Used to sort the tasks")
    date_time: str = Field(None, description="The date and time for the task")
    name: str = Field( None, description="The name of the task")
    details: str = Field(None, description="Additional details about the task")
    
    class Config:
        orm_mode = True
