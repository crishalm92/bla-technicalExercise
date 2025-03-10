from fastapi import APIRouter, HTTPException
from app.domain.schemas.user_schemas import CreateUser, UserSchema
from app.repository.user_repository import UsersRepoImplementation
from app.services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

repo_impl = UsersRepoImplementation()
use_case = UserService(repo_impl)


@router.post("", response_model=UserSchema)
def create_user(user: CreateUser):
    db_user = use_case.get_by_username(username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    user = use_case.create(user)
    return UserSchema(username=user.username, email=user.email)


