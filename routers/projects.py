from fastapi import APIRouter, HTTPException

from db import fetch_all, fetch_one
from routers.tasks import KOLOM as KOLOM_TASK
from schemas import Project, Task

router = APIRouter(prefix="/v1/projects", tags=["projects"])


def cari_project(project_id: int) -> dict:
    project = fetch_one(
        "SELECT * FROM projects WHERE id = %s",
        (project_id,),
    )
    if project is None:
        raise HTTPException(
            status_code=404,
            detail=f"Project {project_id} tidak ditemukan",
        )
    return project


@router.get("", response_model=list[Project])
def daftar_project():
    return fetch_all("SELECT * FROM projects ORDER BY id")


@router.get("/{project_id}", response_model=Project)
def detail_project(project_id: int):
    return cari_project(project_id)


@router.get("/{project_id}/tasks", response_model=list[Task])
def task_milik_project(project_id: int):
    cari_project(project_id)
    return fetch_all(
        f"SELECT {KOLOM_TASK} FROM tasks WHERE project_id = %s ORDER BY id",
        (project_id,),
    )