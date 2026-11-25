from fastapi import APIRouter, HTTPException, Query

from db import execute, fetch_all, fetch_one, insert
from schemas import Status, Task, TaskCreate, TaskUpdate

router = APIRouter(prefix="/v1/tasks", tags=["tasks"])

KOLOM = "id, project_id, title, status, priority, due_date, created_at"


def cari_task(task_id: int) -> dict:
    task = fetch_one(f"SELECT {KOLOM} FROM tasks WHERE id = %s", (task_id,))
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} tidak ditemukan")
    return task

@router.post("", response_model=Task, status_code=201)
def buat_task(body: TaskCreate):
    pastikan_project_ada(body.project_id)
    id_baru = insert(
        "INSERT INTO tasks (project_id, title, status, priority, due_date) "
        "VALUES (%s, %s, %s, %s, %s)",
        (body.project_id, body.title, body.status, body.priority, body.due_date),
    )
    return cari_task(id_baru)


@router.put("/{task_id}", response_model=Task)
def ganti_task(task_id: int, body: TaskCreate):
    cari_task(task_id)
    pastikan_project_ada(body.project_id)
    execute(
        "UPDATE tasks SET project_id = %s, title = %s, status = %s, "
        "priority = %s, due_date = %s WHERE id = %s",
        (
            body.project_id,
            body.title,
            body.status,
            body.priority,
            body.due_date,
            task_id,
        ),
    )
    return cari_task(task_id)


@router.patch("/{task_id}", response_model=Task)
def ubah_sebagian_task(task_id: int, body: TaskUpdate):
    cari_task(task_id)
    perubahan = body.model_dump(exclude_unset=True)

    tidak_boleh_null = [k for k, v in perubahan.items() if v is None and k != "due_date"]
    if tidak_boleh_null:
        raise HTTPException(
            status_code=422,
            detail=f"Field {', '.join(tidak_boleh_null)} tidak boleh null",
        )
    if "project_id" in perubahan:
        pastikan_project_ada(perubahan["project_id"])

    if perubahan:
        set_sql = ", ".join(f"{kolom} = %s" for kolom in perubahan)
        execute(
            f"UPDATE tasks SET {set_sql} WHERE id = %s",
            (*perubahan.values(), task_id),
        )
    return cari_task(task_id)


@router.delete("/{task_id}", status_code=204)
def hapus_task(task_id: int):
    jumlah_terhapus = execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    if jumlah_terhapus == 0:
        raise HTTPException(status_code=404, detail=f"Task {task_id} tidak ditemukan")


def pastikan_project_ada(project_id: int) -> None:
    if fetch_one("SELECT id FROM projects WHERE id = %s", (project_id,)) is None:
        raise HTTPException(status_code=400, detail=f"Project {project_id} tidak ada")


@router.get("", response_model=list[Task])
def daftar_task(
    status: Status | None = None,
    priority: int | None = Query(default=None, ge=1, le=3),
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    syarat = []
    params = []
    if status is not None:
        syarat.append("status = %s")
        params.append(status)
    if priority is not None:
        syarat.append("priority = %s")
        params.append(priority)

    where = f"WHERE {' AND '.join(syarat)}" if syarat else ""
    sql = f"SELECT {KOLOM} FROM tasks {where} ORDER BY id LIMIT %s OFFSET %s"
    params += [limit, offset]
    return fetch_all(sql, tuple(params))


@router.get("/{task_id}", response_model=Task)
def detail_task(task_id: int):
    return cari_task(task_id)
