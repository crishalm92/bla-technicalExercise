from app.repository.config import get_session_local
from app.domain.use_cases.user_use_cases import UserRepository
from .models import models
from app.domain.models import User
from app.domain.schemas.user_schemas import CreateUser


class UsersRepoImplementation(UserRepository):
    _instance = None

    def __new__(cls, *args, **kwargs):
        # Singleton instance to handle unique Session class
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance.db = get_session_local()
        return cls._instance

    def create(self, user: CreateUser) -> User:
        db_user = models.User(
            username=user.username,
            email=user.email,
            password=user.password
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_by_username(self, username: str) -> User:
        return self.db.query(models.User).filter(models.User.username == username).first()
