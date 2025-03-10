from datetime import datetime, date
from app.domain.use_cases.task_use_cases import TaskUseCase, TaskRepository
from app.domain.models import Task, User, TaskStatus
from typing import List


class TaskService(TaskUseCase):

    def __init__(self, repository: TaskRepository):
        self.repo = repository

    def create(
        self, title: str, description: str,
        due_date: datetime,  created_by: User,
        task_code: str = None, assigned_to: User = None
    ):
        new_task = Task(
            title=title, description=description,
            due_date=due_date, created_by=created_by,
            assigned_to=assigned_to
        )
        return self.repo.create(new_task)

    def update(self, task_code: str, updates: dict) -> Task:
        task = self.repo.get(task_code)
        if not task:
            return None
        updated_task = self.repo.update(task, updates)
        return updated_task

    def read(self, task_code: str):
        return self.repo.get(task_code)

    def delete(self, task_code: str) -> bool:
        task = self.read(task_code)
        if not task:
            raise ValueError('Task not found')
        return self.repo.delete(task)

    def filter_by_date_and_status(
            self, date_from: date,
            date_to: date,
            status: TaskStatus,
            page=int,
            size=int
    ):
        tasks, total = self.repo.filter_by_date_and_status(
            status=status, date_from=date_from,
            date_to=date_to, page=page,
            size=size
        )
        return tasks, total

    def update_status(self, task: Task, status: TaskStatus) -> bool: ...

    def get_all(self, username: str) -> List[Task]:
        return self.repo.get_all(username)
