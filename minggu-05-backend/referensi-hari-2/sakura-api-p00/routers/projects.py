from fastapi import APIRouter, HTTPException

from db import fetch_all, fetch_one
from routers.tasks import KOLOM
from schemas import Project, RingkasanProject, Task

router = APIRouter(prefix="/v1/projects", tags=["projects"])


def cari_project(project_id: int) -> dict:
    project = fetch_one(
        "SELECT id, name, client FROM projects WHERE id = %s", (project_id,)
    )
    if project is None:
        raise HTTPException(status_code=404, detail=f"Project {project_id} tidak ditemukan")
    return project


@router.get("", response_model=list[Project])
def daftar_project():
    return fetch_all("SELECT id, name, client FROM projects ORDER BY id")


@router.get("/{project_id}", response_model=Project)
def detail_project(project_id: int):
    return cari_project(project_id)


@router.get("/{project_id}/tasks", response_model=list[Task])
def task_milik_project(project_id: int):
    cari_project(project_id)
    return fetch_all(
        f"SELECT {KOLOM} FROM tasks WHERE project_id = %s ORDER BY id", (project_id,)
    )


# Tantangan (opsional): ringkasan jumlah task per status.
@router.get("/{project_id}/ringkasan", response_model=RingkasanProject)
def ringkasan_project(project_id: int):
    cari_project(project_id)
    rows = fetch_all(
        "SELECT status, COUNT(*) AS jumlah FROM tasks "
        "WHERE project_id = %s GROUP BY status",
        (project_id,),
    )
    hasil = {"project_id": project_id, "todo": 0, "doing": 0, "done": 0}
    for r in rows:
        hasil[r["status"]] = r["jumlah"]
    return hasil
