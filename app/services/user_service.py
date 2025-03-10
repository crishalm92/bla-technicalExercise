from app.domain.use_cases.user_use_cases import UserUseCase, UserRepository
from app.domain.models import User
from app.domain.schemas.user_schemas import CreateUser
from app.api.auth.utils import hash_password


class UserService(UserUseCase):

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create(self, user: CreateUser) -> User:
        user.password = hash_password(user.password)
        return self.repository.create(user)

    def delete(self, user: User) -> bool: ...

    def get_by_username(self, username: str) -> User:
        return self.repository.get_by_username(username)
