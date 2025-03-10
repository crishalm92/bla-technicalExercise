import random
import string
from datetime import datetime
from enum import Enum


def create_random_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))


class TaskStatus(str, Enum):
    NEW = 'new'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'


class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


class Task:
    def __init__(
            self, title: str, description: str,
            due_date: datetime,  created_by: User,
            task_code: str = None, created_at: datetime = None, updated_at: datetime = None,
            assigned_to: User = None, status: TaskStatus = TaskStatus.NEW
    ):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.created_by = created_by
        self.task_code = task_code if task_code else create_random_code()
        self.created_at = created_at if created_at else datetime.utcnow()
        self.updated_at = updated_at if updated_at else datetime.utcnow()
        self.assigned_to = assigned_to
        self.status = status

    def mark_as_completed(self):
        self.status = TaskStatus.COMPLETED
        self.updated_at = datetime.utcnow()
