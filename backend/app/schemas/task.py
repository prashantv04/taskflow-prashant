from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import date

class TaskCreate(BaseModel):
    title: str
    description: Optional[str]
    priority: Optional[str] = "medium"
    assignee_id: Optional[UUID]
    due_date: Optional[date]

class TaskUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    status: Optional[str]
    priority: Optional[str]
    assignee_id: Optional[UUID]
    due_date: Optional[date]