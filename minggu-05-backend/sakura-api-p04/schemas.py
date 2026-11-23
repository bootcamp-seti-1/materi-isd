"""Bentuk data yang masuk (request body) dan keluar (response).

Hari 1: tipe dasar saja. Aturan seperti panjang judul atau batas priority
ditambahkan di Hari 2 (validasi).
"""

from datetime import date
from typing import Literal

from pydantic import BaseModel

Status = Literal["todo", "doing", "done"]


class TaskCreate(BaseModel):
    """Body untuk POST dan PUT: semua field yang wajib dikirim."""

    project_id: int
    title: str
    status: Status = "todo"
    priority: int = 2
    due_date: date | None = None


class TaskUpdate(BaseModel):
    """Body untuk PATCH: semua field boleh tidak dikirim."""

    project_id: int | None = None
    title: str | None = None
    status: Status | None = None
    priority: int | None = None
    due_date: date | None = None


class Task(TaskCreate):
    """Bentuk task yang dikirim balik ke client."""

    id: int


class Project(BaseModel):
    id: int
    name: str
    client: str
