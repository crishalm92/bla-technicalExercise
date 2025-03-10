from datetime import datetime, date
from typing import List
from app.repository.config import get_session_local
from app.domain.use_cases.task_use_cases import TaskRepository
from app.domain.models import Task, TaskStatus
from app.repository.models import models as RepoModels


class TaskRepoImplementation(TaskRepository):
    _instance = None

    def __new__(cls, *args, **kwargs):
        # Singleton instance to handle unique Session class
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance.db = get_session_local()
        return cls._instance

    def create(self, task: Task) -> Task:
        new_task = RepoModels.Task(
            title=task.title, description=task.description,
            created_at=task.created_at, updated_at=task.updated_at,
            due_date=task.due_date, task_code=task.task_code,
            status=task.status)
        created_by = self.db.query(RepoModels.User).filter(
            RepoModels.User.username == task.created_by.username
        ).first()
        new_task.created_by = created_by
        if task.assigned_to:
            if task.created_by == task.assigned_to:
                new_task.assigned_to = task.assigned_to
            else:
                assigned_to = self.db.query(RepoModels.User).filter(
                    RepoModels.User.username == task.assigned_to.username
                ).first()
                new_task.assigned_to = assigned_to
        self.db.add(new_task)
        self.db.commit()
        self.db.refresh(new_task)
        return task

    def update(self, task: Task, updates: dict) -> Task:
        for key, value in updates.items():
            if value is not None:
                if key == 'assigned_to':
                    value = self.db.query(RepoModels.User).filter(RepoModels.User.username == value).first()
                setattr(task, key, value)
        task.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete(self, task: Task) -> bool:
        task = self.db.query(RepoModels.Task).filter(
            RepoModels.Task.task_code == task.task_code
        ).first()
        if task:
            self.db.delete(task)
            self.db.commit()
            return True
        return False

    def get(self, task_code: str) -> Task:
        return self.db.query(RepoModels.Task).filter(RepoModels.Task.task_code == task_code).first()

    def filter_by_date_and_status(
        self, date_from: date,
        date_to: date,
        status: TaskStatus,
        page=int,
        size=int
    ):
        query = self.db.query(RepoModels.Task)
        if status:
            query = query.filter(RepoModels.Task.status == status)
        if date_from:
            from_datetime = datetime.combine(date_from, datetime.min.time())  # 00:00:00 value
            query = query.filter(RepoModels.Task.due_date >= from_datetime)
        if date_to:
            to_datetime = datetime.combine(date_to, datetime.max.time())  # 23:59:59 of the day
            query = query.filter(RepoModels.Task.due_date <= to_datetime)
        total = query.count()
        tasks = query.offset((page - 1) * size).limit(size).all()
        return tasks, total

    def get_all(self, username) -> List[Task]:
        # Return a list of all task associated to specific user
        user = self.db.query(RepoModels.User).filter(RepoModels.User.username == username).first()
        tasks_assigned = self.db.query(RepoModels.Task).filter(RepoModels.Task.created_by_id == user.id).all()
        return tasks_assigned
