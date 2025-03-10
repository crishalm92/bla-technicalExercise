from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.domain.models import TaskStatus

class CreateTask(BaseModel):
    title: str
    description: str
    due_date: datetime
    assigned_to: Optional[str] = None


class ResponseTask(CreateTask):
    created_by: str
    task_code: str
    created_at: datetime
    status: TaskStatus


class UpdateTask(CreateTask):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    status: Optional[TaskStatus] = None


class TaskFilter(BaseModel):
    total: int
    page: int
    size: int
    tasks: List[ResponseTask]