from abc import ABC, abstractmethod
from typing import List
from datetime import datetime, date
from app.domain.models import Task, TaskStatus, User


class TaskUseCase(ABC):
    @abstractmethod
    def create(
        self, title: str, description: str,
        due_date: datetime,  created_by: User,
        task_code: str = None, assigned_to: User = None
    ): ...

    @abstractmethod
    def update(self, task_code: str, updates: dict) -> Task: ...

    @abstractmethod
    def read(self, task_code: str): ...

    @abstractmethod
    def delete(self, task_code: str) -> bool: ...

    @abstractmethod
    def filter_by_date_and_status(
            self, date_from: date,
            date_to: date,
            status: TaskStatus,
            page=int,
            size=int
    ): ...

    @abstractmethod
    def update_status(self, task: Task, status: TaskStatus) -> Task: ...

    @abstractmethod
    def get_all(self, username: str) -> List[Task]: ...


class TaskRepository(ABC):
    @abstractmethod
    def create(self, task: Task) -> Task: ...

    @abstractmethod
    def update(self, task: Task, updates: dict) -> Task: ...

    @abstractmethod
    def delete(self, task: Task) -> bool: ...

    @abstractmethod
    def get(self, task_code: str) -> Task: ...

    @abstractmethod
    def filter_by_date_and_status(
            self, date_from: date,
            date_to: date,
            status: TaskStatus,
            page=int,
            size=int
    ): ...

    @abstractmethod
    def get_all(self, username) -> List[Task]: ...
