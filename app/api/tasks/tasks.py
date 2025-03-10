from fastapi import APIRouter, Request, HTTPException, Query
from typing import Optional
from datetime import date
from app.repository.task_repository import TaskRepoImplementation
from app.repository.user_repository import UsersRepoImplementation
from app.services.task_service import TaskService
from app.services.user_service import UserService
from app.api.auth.decorators import requires_auth
from app.domain.schemas.task_schemas import ResponseTask, CreateTask, UpdateTask, TaskFilter
from app.domain.models import TaskStatus


router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    responses={404: {"description": "Not found"}},
)
task_repo = TaskRepoImplementation()
user_repo = UsersRepoImplementation()
task_use_case = TaskService(task_repo)
user_use_case = UserService(user_repo)

@router.get("/all/")
@requires_auth
async def get_all_tasks(request: Request):
    items = task_use_case.get_all(request.state.user)
    return items

@router.post("/create/", response_model=ResponseTask, status_code=201)
@requires_auth
async def create_task(request: Request, task_request: CreateTask):
    user = user_use_case.get_by_username(username=request.state.user)
    assigned_user = None
    if task_request.assigned_to:
        assigned_user = user_use_case.get_by_username(username=task_request.assigned_to)
    task = task_use_case.create(
        title=task_request.title, description=task_request.title,
        due_date=task_request.due_date, created_by=user,
        assigned_to=assigned_user
    )
    response_task = ResponseTask(
        title=task.title, description=task.description,
        due_date=task.due_date, status=task.status,
        created_by=task.created_by.username, task_code=task.task_code,
        created_at=task.created_at, assigned_to=None
    )
    if task.assigned_to:
        response_task.assigned_to = task.assigned_to.username
    return response_task


@router.put("/{task_code}", response_model=ResponseTask)
@requires_auth
async def update_task(request: Request, task_code: str, updates: UpdateTask):
    task_data = updates.dict(exclude_unset=True)
    task = task_use_case.update(task_code, task_data)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    response_task = ResponseTask(
        title=task.title, description=task.description,
        due_date=task.due_date, status=task.status,
        created_by=task.created_by.username, task_code=task.task_code,
        created_at=task.created_at, assigned_to=None
    )
    if task.assigned_to:
        response_task.assigned_to = task.assigned_to.username
    return response_task


@router.get("/task/{task_code}", response_model=ResponseTask)
@requires_auth
async def get_task(request: Request, task_code: str):
    task = task_use_case.read(task_code)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    response_task = ResponseTask(
        title=task.title, description=task.description,
        due_date=task.due_date, status=task.status,
        created_by=task.created_by.username, task_code=task.task_code,
        created_at=task.created_at, assigned_to=None
    )
    if task.assigned_to:
        response_task.assigned_to = task.assigned_to.username
    return response_task


@router.delete("/{task_code}", status_code=204)
@requires_auth
async def delete_task(request: Request, task_code: str):
    task = task_use_case.read(task_code)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    # Only creator user can delete task
    if task.created_by.username != request.state.user:
        raise HTTPException(status_code=403, detail="Not authorized to delete this task")
    task_use_case.delete(task_code)
    return {"message": "Task deleted successfully"}


@router.put("/complete/{task_code}", status_code=201)
@requires_auth
async def complete_task(request: Request, task_code: str):
    task = task_use_case.update(task_code, {'status': TaskStatus.COMPLETED})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task completed!"}


@router.get("/filter", status_code=200, response_model=TaskFilter)
@requires_auth
async def filter_tasks(
    request: Request,
    status: Optional[TaskStatus] = Query(None, description="Filter by task status"),
    date_from: Optional[date] = Query(None, description="Start date (YYYY-MM-DD)"),
    date_to: Optional[date] = Query(None, description="End date (YYYY-MM-DD)"),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, le=100, description="Number of tasks per page")
):
    tasks, total = task_use_case.filter_by_date_and_status(
        status=status, date_from=date_from, date_to=date_to,
        page=page, size=size
    )
    tasks_response = [
        ResponseTask(
            title=task.title,
            description=task.description,
            due_date=task.due_date,
            assigned_to=task.assigned_to.username if task.assigned_to else None,
            created_by=task.created_by.username,
            task_code=task.task_code,
            created_at=task.created_at,
            status=task.status
        ) for task in tasks
    ]
    return TaskFilter(
        total=total, page=page, size=size,
        tasks=tasks_response
    )
