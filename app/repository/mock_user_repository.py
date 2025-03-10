from app.domain.use_cases.user_use_cases import UserRepository
from .models import models
from app.domain.models import User
from app.domain.schemas.user_schemas import CreateUser


class UsersRepoImplementation(UserRepository):

    def create(self, user: CreateUser) -> User:
        return models.User(
            username=user.username,
            email=user.email,
            password=user.password
        )

    def get_by_username(self, username: str) -> User:
        if username != 'valid_user':
            return User(username=username, email='not_real@email.com', password='text')
        return None
