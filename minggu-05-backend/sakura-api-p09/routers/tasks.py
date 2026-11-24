from fastapi import APIRouter, HTTPException, Query

from data import PROJECTS, TASKS, id_berikutnya
from schemas import Status, Task, TaskCreate, TaskUpdate

# Membuat kelompok router dengan awalan URL "/v1/tasks" dan pengelompokan "tasks" di /docs
router = APIRouter(prefix="/v1/tasks", tags=["tasks"])


# Fungsi bantu mencari task berdasarkan ID.
# Jika ketemu, kembalikan dictionary task-nya; jika tidak ada, lempar error HTTP 404.
def cari_task(task_id: int) -> dict:
    for task in TASKS:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail=f"Task dengan id {task_id} tidak ditemukan")


# Fungsi bantu memastikan project_id yang dikirim user benar-benar ada di PROJECTS.
# Mencegah pembuatan/pemindahan task ke project yang fiktif (error 404).
def pastikan_project_ada(project_id: int) -> None:
    if not any(p["id"] == project_id for p in PROJECTS):
        raise HTTPException(status_code=404, detail=f"Project dengan id {project_id} tidak ditemukan")


# READ (Semua + Filter): GET /v1/tasks
# Mendukung filter opsional lewat query parameter (?status=...&project_id=...&q=...)
@router.get("", response_model=list[Task])
def daftar_task(
    status: Status | None = None,                    # Divalidasi harus "todo", "doing", atau "done"
    project_id: int | None = None,                   # Filter berdasarkan ID project
    q: str | None = Query(default=None, min_length=1), # Pencarian kata kunci pada judul (minimal 1 huruf)
):
    hasil = TASKS
    if status is not None:
        hasil = [t for t in hasil if t["status"] == status]
    if project_id is not None:
        hasil = [t for t in hasil if t["project_id"] == project_id]
    if q is not None:
        hasil = [t for t in hasil if q.lower() in t["title"].lower()]
    return hasil


# READ (Satu Data): GET /v1/tasks/{task_id}
@router.get("/{task_id}", response_model=Task)
def detail_task(task_id: int):
    return cari_task(task_id)


# CREATE: POST /v1/tasks
# Mengembalikan status HTTP 201 (Created) jika berhasil membuat task baru
@router.post("", response_model=Task, status_code=201)
def buat_task(body: TaskCreate):
    pastikan_project_ada(body.project_id)
    # Menggabungkan ID baru dengan seluruh field input dari body JSON
    task_baru = {"id": id_berikutnya(TASKS), **body.model_dump()}
    TASKS.append(task_baru)
    return task_baru


# UPDATE UTUH (Replace): PUT /v1/tasks/{task_id}
# Menimpa seluruh isi task dengan data baru; field opsional yang tidak dikirim akan kembali ke nilai default
@router.put("/{task_id}", response_model=Task)
def ganti_task(task_id: int, body: TaskCreate):
    task = cari_task(task_id)
    pastikan_project_ada(body.project_id)
    task.update(body.model_dump())
    return task


# UPDATE SEBAGIAN (Partial): PATCH /v1/tasks/{task_id}
# Hanya mengubah field yang benar-benar dikirim oleh user (exclude_unset=True)
@router.patch("/{task_id}", response_model=Task)
def ubah_sebagian_task(task_id: int, body: TaskUpdate):
    task = cari_task(task_id)
    data_perubahan = body.model_dump(exclude_unset=True)
    # Jika user ikut mengubah project_id, pastikan project tujuan tersebut ada
    if "project_id" in data_perubahan:
        pastikan_project_ada(data_perubahan["project_id"])
    task.update(data_perubahan)
    return task


# DELETE: DELETE /v1/tasks/{task_id}
# Menghapus task dan mengembalikan status 204 (No Content / tanpa body respons)
@router.delete("/{task_id}", status_code=204)
def hapus_task(task_id: int):
    task = cari_task(task_id)
    TASKS.remove(task) 