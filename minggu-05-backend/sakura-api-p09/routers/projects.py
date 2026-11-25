from fastapi import APIRouter, HTTPException

from data import PROJECTS, TASKS
from schemas import Project, Task

# Membuat kelompok router dengan awalan URL "/v1/projects" dan pengelompokan "projects" di /docs
router = APIRouter(prefix="/v1/projects", tags=["projects"])


# Fungsi bantu mencari project berdasarkan ID; melempar 404 jika tidak ditemukan
def cari_project(project_id: int) -> dict:
    for project in PROJECTS:
        if project["id"] == project_id:
            return project
    raise HTTPException(status_code=404, detail=f"Project dengan id {project_id} tidak ditemukan")


# GET /v1/projects — Menampilkan semua daftar project
@router.get("", response_model=list[Project])
def daftar_project():
    return PROJECTS


# GET /v1/projects/{project_id} — Menampilkan detail satu project berdasarkan ID
@router.get("/{project_id}", response_model=Project)
def detail_project(project_id: int):
    return cari_project(project_id)


# GET /v1/projects/{project_id}/tasks — Menampilkan semua task milik project tertentu
@router.get("/{project_id}/tasks", response_model=list[Task])
def daftar_task_project(project_id: int):
    # Pastikan project-nya ada dulu (jika ID 99 tidak ada, otomatis stop dan return 404)
    cari_project(project_id)
    # Saring dan kembalikan hanya task yang memiliki project_id sesuai parameter URL
    return [t for t in TASKS if t["project_id"] == project_id] 