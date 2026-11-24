from fastapi import APIRouter, HTTPException

from data import PROJECTS, TASKS
from schemas import Project, Task

router = APIRouter(prefix="/v1/projects", tags=["projects"])


def cari_project(project_id: int) -> dict:
    for p in PROJECTS:
        if p["id"] == project_id:
            return p
    raise HTTPException(
        status_code=404,
        detail=f"Project {project_id} tidak ditemukan",
    )


@router.get("", response_model=list[Project])
def daftar_project():
    return PROJECTS


@router.get("/{project_id}", response_model=Project)
def detail_project(project_id: int):
    return cari_project(project_id)


@router.get("/{project_id}/tasks", response_model=list[Task])
def task_project(project_id: int):
    cari_project(project_id)
    return [t for t in TASKS if t["project_id"] == project_id]