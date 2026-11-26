from datetime import date
from typing import Literal

from pydantic import BaseModel

Status = Literal["todo", "doing", "done"]


class TaskCreate(BaseModel):
    project_id: int
    title: str
    status: Status = "todo"
    priority: int = 2
    due_date: date | None = None


class TaskUpdate(BaseModel):
    project_id: int | None = None
    title: str | None = None
    status: Status | None = None
    priority: int | None = None
    due_date: date | None = None


class Task(TaskCreate):
    id: int


class Project(BaseModel):
    id: int
    name: str
    client: str