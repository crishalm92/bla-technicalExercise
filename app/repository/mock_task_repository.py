from datetime import datetime, date
from typing import List
from app.domain.use_cases.task_use_cases import TaskRepository
from app.domain.models import Task, TaskStatus, User


mock_user = User(
    username='test_user',
    email='example@mail.com',
    password='password'
)


class TaskRepoImplementation(TaskRepository):
    def create(self, task: Task) -> Task:
        return task

    def update(self, task: Task, updates: dict) -> Task:
        for key, value in updates.items():
            if value is not None:
                if key == 'assigned_to':
                    value = mock_user
                setattr(task, key, value)
        task.updated_at = datetime.utcnow()
        return task

    def delete(self, task: Task) -> bool:
        return True

    def get(self, task_code: str) -> Task:
        # return test_code only
        user = User
        if task_code == "test_code":
            return Task(
                task_code="test_code",
                title="Test Task",
                description="Test Task Description",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                status=TaskStatus.NEW,
                due_date=datetime.utcnow(),
                created_by=mock_user
            )
        return None

    def filter_by_date_and_status(
        self, date_from: date,
        date_to: date,
        status: TaskStatus,
        page=int,
        size=int
    ):
        return [
            Task(
                task_code="filtered_code_1",
                title="Filtered Task 1",
                description="Filtered Task 1 Description",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                status=status,
                due_date=datetime.utcnow(),
                created_by=mock_user
            )
        ], 1

    def get_all(self, username) -> List[Task]:
        return [
            Task(
                task_code="test_code_1",
                title="Task 1",
                description="Test Task 1",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                status=TaskStatus.NEW,
                due_date=datetime.utcnow(),
                created_by=mock_user
            ),
            Task(
                task_code="test_code_2",
                title="Task 2",
                description="Test Task 2",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                status=TaskStatus.COMPLETED,
                due_date=datetime.utcnow(),
                created_by=mock_user
            ),
        ]
