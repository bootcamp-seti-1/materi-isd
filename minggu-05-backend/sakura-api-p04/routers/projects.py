
from fastapi import APIRouter, HTTPException

from db import fetch_all, fetch_one
from schemas import Project, Task
from routers.tasks import KOLOM

router = APIRouter(prefix="/v1/projects", tags=["projects"])


@router.get("", response_model=list[Project])
def daftar_project():
    sql = """
        SELECT id, name, client
        FROM projects
        ORDER BY id
    """
    return fetch_all(sql)


@router.get("/{project_id}", response_model=Project)
def detail_project(project_id: int):
    sql = """
        SELECT id, name, client
        FROM projects
        WHERE id = %s
    """

    project = fetch_one(sql, (project_id,))

    if project is None:
        raise HTTPException(
            status_code=404,
            detail=f"Project {project_id} tidak ditemukan"
        )

    return project


@router.get("/{project_id}/tasks", response_model=list[Task])
def task_milik_project(project_id: int):
    sql = f"""
        SELECT {KOLOM}
        FROM tasks
        WHERE project_id = %s
        ORDER BY id
    """

    return fetch_all(sql, (project_id,))


@router.get("/{project_id}/ringkasan")
def ringkasan_project(project_id: int):
    # Pastikan project tersedia
    project = fetch_one(
        "SELECT id FROM projects WHERE id = %s",
        (project_id,)
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail=f"Project {project_id} tidak ditemukan"
        )

    # Menghitung task berdasarkan status
    sql = """
        SELECT status, COUNT(*) AS jumlah
        FROM tasks
        WHERE project_id = %s
        GROUP BY status
    """

    hasil = fetch_all(sql, (project_id,))

    # Nilai awal setiap status adalah 0
    ringkasan = {
        "project_id": project_id,
        "todo": 0,
        "doing": 0,
        "done": 0
    }

    # Mengisi jumlah berdasarkan hasil query
    for row in hasil:
        ringkasan[row["status"]] = row["jumlah"]

    return ringkasan
