from fastapi import APIRouter, HTTPException, Query

from data import PROJECTS, TASKS, id_berikutnya
from schemas import Status, Task, TaskCreate, TaskUpdate

router = APIRouter(prefix="/v1/tasks", tags=["tasks"])


def cari_task(task_id: int) -> dict:
    for t in TASKS:
        if t["id"] == task_id:
            return t
    raise HTTPException(status_code=404, detail=f"Task {task_id} tidak ditemukan")


def pastikan_project_ada(project_id: int) -> None:
    if not any(p["id"] == project_id for p in PROJECTS):
        raise HTTPException(status_code=400, detail=f"Project {project_id} tidak ada")


@router.get("", response_model=list[Task])
def daftar_task(
    status: Status | None = None,
    priority: int | None = None,
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    hasil = TASKS
    if status is not None:
        hasil = [t for t in hasil if t["status"] == status]
    if priority is not None:
        hasil = [t for t in hasil if t["priority"] == priority]
    return hasil[offset : offset + limit]


@router.get("/{task_id}", response_model=Task)
def detail_task(task_id: int):
    return cari_task(task_id)


@router.post("", response_model=Task, status_code=201)
def buat_task(body: TaskCreate):
    pastikan_project_ada(body.project_id)
    task_baru = {"id": id_berikutnya(TASKS), **body.model_dump()}
    TASKS.append(task_baru)
    return task_baru


@router.put("/{task_id}", response_model=Task)
def ganti_task(task_id: int, body: TaskCreate):
    task = cari_task(task_id)
    pastikan_project_ada(body.project_id)
    task.update(body.model_dump())
    return task


@router.patch("/{task_id}", response_model=Task)
def ubah_sebagian_task(task_id: int, body: TaskUpdate):
    task = cari_task(task_id)
    perubahan = body.model_dump(exclude_unset=True)
    if "project_id" in perubahan:
        pastikan_project_ada(perubahan["project_id"])
    task.update(perubahan)
    return task


@router.delete("/{task_id}", status_code=204)
def hapus_task(task_id: int):
    task = cari_task(task_id)
    TASKS.remove(task)