from abc import ABC, abstractmethod
from app.domain.models import User
from app.domain.schemas.user_schemas import CreateUser


class UserUseCase(ABC):
    @abstractmethod
    def create(self, user: CreateUser) -> User: ...

    @abstractmethod
    def delete(self, user: User) -> bool: ...

    @abstractmethod
    def get_by_username(self, username: str) -> User: ...


class UserRepository(ABC):
    @abstractmethod
    def get_by_username(self, username: str) -> User: ...

    @abstractmethod
    def create(self, user: CreateUser) -> User: ...

