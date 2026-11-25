from datetime import date
from typing import Literal

from pydantic import BaseModel

# Membatasi nilai status yang sah hanya boleh salah satu dari 3 teks ini.
# Jika user mengirim nilai lain (misal: "selesai"), FastAPI otomatis menolak (422).
Status = Literal["todo", "doing", "done"]


# Skema data untuk resource Project saat dikirim sebagai respons JSON
class Project(BaseModel):
    id: int
    name: str
    client: str


# Skema data yang wajib/boleh dikirim user saat membuat (POST) atau mengganti utuh (PUT) sebuah task.
# Tidak ada field 'id' karena 'id' dibuat otomatis oleh server.
class TaskCreate(BaseModel):
    project_id: int
    title: str
    status: Status = "todo"        # Nilai bawaan jika tidak diisi adalah "todo"
    priority: int = 2              # Nilai bawaan jika tidak diisi adalah 2
    due_date: date | None = None   # Boleh dikosongkan (None); jika diisi harus format tanggal (YYYY-MM-DD)


# Skema data lengkap sebuah Task (mewarisi semua field dari TaskCreate + tambahan 'id').
# Digunakan sebagai response_model saat menampilkan data task ke user.
class Task(TaskCreate):
    id: int


# Skema data khusus untuk update sebagian (PATCH).
# Semua field diberi nilai default None agar user cukup mengirim field yang ingin diubah saja.
class TaskUpdate(BaseModel):
    project_id: int | None = None
    title: str | None = None
    status: Status | None = None
    priority: int | None = None
    due_date: date | None = None