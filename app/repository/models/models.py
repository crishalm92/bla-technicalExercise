from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.repository.config import get_base_db_type
from app.domain.models import TaskStatus

Base_db = get_base_db_type()


class Task(Base_db):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    due_date = Column(DateTime, nullable=True)
    task_code = Column(String, unique=True, index=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.NEW, nullable=False)

    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_to_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    created_by = relationship("User", back_populates="tasks_created", foreign_keys=[created_by_id])
    assigned_to = relationship("User", back_populates="tasks_assigned", foreign_keys=[assigned_to_id])


class User(Base_db):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    tasks_created = relationship("Task", back_populates="created_by", foreign_keys=[Task.created_by_id])
    tasks_assigned = relationship("Task", back_populates="assigned_to", foreign_keys=[Task.assigned_to_id])
