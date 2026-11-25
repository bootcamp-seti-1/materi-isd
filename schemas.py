from datetime import date
from typing import Literal
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

Status = Literal["todo", "doing", "done"]


class Masukan(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )


def cek_tanggal(nilai):
    if nilai is not None and nilai < date.today():
        raise ValueError("due_date tidak boleh tanggal yang sudah lewat")
    return nilai


class TaskCreate(Masukan):
    project_id: int = Field(gt=0)
    title: str = Field(min_length=3, max_length=150)
    status: Status = "todo"
    priority: int = Field(default=2, ge=1, le=3)
    due_date: date | None = None

    @field_validator("due_date")
    @classmethod
    def validasi_due_date(cls, nilai):
        return cek_tanggal(nilai)


class TaskUpdate(Masukan):
    project_id: int | None = Field(default=None, gt=0)
    title: str | None = Field(default=None, min_length=3, max_length=150)
    status: Status | None = None
    priority: int | None = Field(default=None, ge=1, le=3)
    due_date: date | None = None

    @field_validator("due_date")
    @classmethod
    def validasi_due_date(cls, nilai):
        return cek_tanggal(nilai)


class Task(BaseModel):
    id: int
    project_id: int
    title: str
    status: Status
    priority: int
    due_date: date | None
    created_at: datetime


class Project(BaseModel):
    id: int
    name: str
    client: str

class RingkasanProject(BaseModel):
    project_id: int
    todo: int
    doing: int
    done: int