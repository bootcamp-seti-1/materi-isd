# Hari 2 — Hands-on: validasi dan MySQL untuk Sakura Tasks API

Ikuti langkahnya berurutan, ketik persis, dan cocokkan hasilmu di setiap titik cek. Penjelasan disampaikan trainer sambil mengetik.

Kemarin API-mu sudah lengkap, tapi ada dua masalah: datanya hilang setiap server restart, dan API masih menerima data aneh seperti judul satu huruf atau priority 99. Hari ini dua masalah itu diselesaikan: aturan data diperketat, lalu penyimpanan dipindah ke MySQL `sakura_db` milikmu dari minggu 3. Alamat endpoint-nya **tidak berubah sama sekali**.

## Tujuan hari ini

Mas Bayu menunjukkan laporan dari tim frontend:

> "Ada yang iseng kirim task dengan judul spasi doang, priority 99, tanggal tahun 2020. API kita terima semua. Terus kemarin server sempat restart, semua task yang mereka buat hilang. Hari ini dua-duanya harus beres: data ngawur ditolak, dan data disimpan di database beneran."

### Hasil akhir yang dikejar hari ini

```text
minggu-05-backend/
  sakura-api-p00/
    .env              user dan password MySQL (TIDAK di-push)
    .env.example      contoh isi .env (di-push)
    db.py             penghubung ke MySQL, membaca .env
    main.py           + penanganan error database
    schemas.py        + aturan validasi
    routers/
      tasks.py        semua endpoint memakai MySQL
      projects.py     semua endpoint memakai MySQL
```

`data.py` dihapus di akhir hari, karena sudah tidak dipakai.

Server sekarang dijalankan dengan:

```text
uv run --env-file .env fastapi dev main.py
```

## Persiapan sebelum mulai

- [ ] Hari 1 selesai: `sakura-api-p00` jalan dan 8 endpoint bekerja (kalau belum, pakai Jalur kejar Hari 1)
- [ ] Folder minggu 3 `sakura-tasks-p00` masih ada, berisi `db/schema.sql` dan `db/seed.sql`
- [ ] Aku ingat user MySQL-ku (`sakura_p00`, ganti dengan ID-mu) dan password-nya (`sakura123`)

## Peta Hari 2 (115 menit)

| Bagian | Isi | Menit | Hasilnya |
| --- | --- | --- | --- |
| A | Persiapan dan reset data | 10 | MySQL menyala, data kembali ke keadaan awal |
| B | Validasi: menolak data ngawur | 20 | Aturan di `schemas.py` |
| C | Sambungan ke MySQL lewat `.env` | 10 | `db.py` baru, password keluar dari kode |
| D | Membaca dari MySQL: GET | 20 | Daftar, filter, pagination, detail dari database |
| E | Menulis ke MySQL: POST, PATCH, PUT, DELETE | 30 | CRUD lengkap tersimpan di database |
| F | Project dari MySQL dan penanganan error | 15 | Semua endpoint pakai database, error rapi |
| G | Simpan ke Git dan GitHub | 10 | Pekerjaan ter-push, `.env` tidak ikut |

## Aturan main

1. Ikuti bagian dari A sampai G, berurutan.
2. Ketik hanya isi kotak berlabel **Ketik** atau **Isi file**. Sisanya dibaca saja.
3. Setiap bagian ditutup **Titik cek**. Cocok? Lanjut.
4. Tertinggal? Pakai **Jalur kejar** di bagian bawah, tidak perlu menunggu siapa pun.
5. Stuck? Tulis di grup: ID, bagian, dan tempel pesan error. Contoh: "P08 stuck di E2".
6. Boleh bertanya ke AI atau mencari di internet. Tapi kamu harus bisa menjelaskan sendiri apa yang kamu ketik.

Seperti kemarin, pakai **dua terminal**: Terminal 1 untuk server, Terminal 2 untuk `curl`. Label-label di lembar ini sama dengan Hari 1.

### Kamus mini

| Kata | Artinya | Contoh |
| --- | --- | --- |
| Validasi | Memeriksa data yang masuk sebelum dipakai | judul minimal 3 huruf |
| `Field` | Tempat menulis aturan untuk satu field Pydantic | `Field(ge=1, le=3)` |
| `ge`, `le`, `gt` | lebih besar atau sama dengan, lebih kecil atau sama dengan, lebih besar dari | `ge=1` artinya minimal 1 |
| Validator | Fungsi untuk aturan yang tidak bisa ditulis dengan `Field` | tanggal tidak boleh sudah lewat |
| Environment variable | Pengaturan yang dibaca program dari luar kode | `DB_PASSWORD` |
| `.env` | File berisi environment variable | `DB_USER=sakura_p00` |
| `lastrowid` | `id` yang baru dibuat MySQL setelah `INSERT` | `9` |
| `rowcount` | Jumlah baris yang terkena `UPDATE` atau `DELETE` | `0` kalau id tidak ada |

---

## Bagian A — Persiapan dan reset data (10 menit)

### A1 — Nyalakan MySQL

**Ketik di terminal:**

```text
sudo service mysql start
```

### A2 — Kembalikan data Sakura Tasks ke keadaan awal

Supaya hasil semua peserta sama, tabel `projects` dan `tasks` dibuat ulang dari file minggu 3. Tabel perpustakaan (`books`, `members`, `loans`) tidak tersentuh.

**Ketik di terminal** (ganti `p00` dengan ID-mu):

```text
cd ~/seti-isd-materi/minggu-03-database/sakura-tasks-p00
```

```text
mysql -u sakura_p00 -p sakura_db < db/schema.sql
```

```text
mysql -u sakura_p00 -p sakura_db < db/seed.sql
```

Password: `sakura123`. Kalau muncul `No such file or directory` untuk `seed.sql`, buka Jalur kejar bagian "Kalau seed.sql tidak ada".

### A3 — Cek datanya

```text
mysql -u sakura_p00 -p sakura_db -e "SELECT id, project_id, title, status, priority FROM tasks"
```

**Yang harus muncul di layar:** 8 baris task, id 1 sampai 8.

### A4 — Masuk ke proyek API dan pasang penghubung MySQL

```text
cd ~/seti-isd-materi/minggu-05-backend/sakura-api-p00
```

```text
uv add mysql-connector-python
```

```text
code .
```

### Titik cek A

- [ ] Tabel `tasks` berisi 8 baris
- [ ] `pyproject.toml` di `sakura-api-p00` sekarang memuat `mysql-connector-python`

---

## Bagian B — Validasi: menolak data ngawur (20 menit)

Bagian ini masih memakai data di memori dari kemarin. Database baru dipakai di Bagian C.

### B1 — Coba dulu kirim data ngawur

Jalankan server seperti kemarin.

**Terminal 1:**

```text
uv run fastapi dev main.py
```

**Terminal 2:**

```text
curl -i -X POST http://localhost:8000/v1/tasks -H "Content-Type: application/json" -d '{"project_id": 1, "title": " ", "priority": 99, "due_date": "2020-01-01", "assignee": "Budi"}'
```

**Yang harus muncul di layar:** `201 Created`. API menerima judul spasi, priority 99, tanggal 2020, dan diam-diam membuang `assignee`. Ini yang akan diperbaiki.

### B2 — Aturan baru di schemas.py

**File:** `schemas.py`, ganti seluruh isinya.

**Isi file:**

```python
from datetime import date
from typing import Literal

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


class Project(BaseModel):
    id: int
    name: str
    client: str
```

Perhatikan: `Task` (bentuk response) sekarang **tidak lagi** turunan `TaskCreate`. Aturan untuk data yang masuk tidak berlaku untuk data yang keluar. Contohnya, task lama yang tanggalnya sudah lewat tetap boleh ditampilkan.

### B3 — Kirim ulang data ngawur, satu per satu

**Terminal 2:**

```text
curl -s -X POST http://localhost:8000/v1/tasks -H "Content-Type: application/json" -d '{"project_id": 1, "title": " "}' | python3 -m json.tool
```

```text
curl -s -X POST http://localhost:8000/v1/tasks -H "Content-Type: application/json" -d '{"project_id": 1, "title": "Uji", "priority": 99}' | python3 -m json.tool
```

```text
curl -s -X POST http://localhost:8000/v1/tasks -H "Content-Type: application/json" -d '{"project_id": 1, "title": "Uji", "due_date": "2020-01-01"}' | python3 -m json.tool
```

```text
curl -s -X POST http://localhost:8000/v1/tasks -H "Content-Type: application/json" -d '{"project_id": 1, "title": "Uji", "assignee": "Budi"}' | python3 -m json.tool
```

```text
curl -s -X POST http://localhost:8000/v1/tasks -H "Content-Type: application/json" -d '{"project_id": 1, "title": "   Cetak laporan   "}' | python3 -m json.tool
```

Bacalah setiap pesan error. Di dalam `"detail"`, bagian `"loc"` menunjukkan field mana yang salah, dan `"msg"` menjelaskan kenapa.

### Titik cek B

- [ ] Judul spasi saja → `422`, pesannya tentang panjang minimal (spasi dibuang dulu, sisanya kosong)
- [ ] `priority` 99 → `422`, `less than or equal to 3`
- [ ] `due_date` 2020 → `422`, pesannya `due_date tidak boleh tanggal yang sudah lewat`
- [ ] Field `assignee` → `422`, `Extra inputs are not permitted`
- [ ] `"   Cetak laporan   "` diterima dan tersimpan sebagai `"Cetak laporan"`
- [ ] Di `/docs`, bagian **Schemas** menampilkan aturan baru (minLength, maximum, dan seterusnya)

**Dibahas trainer:**

- Kenapa validasi harus di backend walaupun frontend juga memeriksa. Siapa saja bisa memanggil API pakai `curl`, seperti yang baru kamu lakukan.
- Tiga lapis pemeriksaan: tipe (`int`, `date`), aturan `Field`, dan validator buatan sendiri.
- Kenapa model masukan (`TaskCreate`, `TaskUpdate`) dipisah dari model keluaran (`Task`).
- `extra="forbid"`: lebih baik menolak dengan jelas daripada membuang diam-diam. Validasi input juga dibahas lagi di modul Security.

---

## Bagian C — Sambungan ke MySQL lewat .env (10 menit)

Di minggu 3, password ditulis langsung di `db.py`. Kalau di-push, password itu terbaca siapa saja di GitHub. Sekarang password dipindah ke file `.env` yang tidak ikut di-push.

### C1 — File .env dan contohnya

**File (baru):** `.env` (ganti `p00` dengan ID-mu)

**Isi file:**

```text
DB_HOST=127.0.0.1
DB_USER=sakura_p00
DB_PASSWORD=sakura123
DB_NAME=sakura_db
```

**File (baru):** `.env.example`

**Isi file:**

```text
DB_HOST=127.0.0.1
DB_USER=sakura_p00
DB_PASSWORD=ganti_dengan_password
DB_NAME=sakura_db
```

### C2 — Pastikan .env tidak ikut Git

Buka `.gitignore`, tambahkan satu baris di paling bawah, lalu simpan:

```text
.env
```

### C3 — db.py baru

**File (baru):** `db.py`

**Isi file:**

```python
import os

import mysql.connector

DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "127.0.0.1"),
    "user": os.environ["DB_USER"],
    "password": os.environ["DB_PASSWORD"],
    "database": os.environ.get("DB_NAME", "sakura_db"),
}


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def fetch_all(sql, params=()):
    conn = get_connection()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, params)
        return cur.fetchall()
    finally:
        conn.close()


def fetch_one(sql, params=()):
    rows = fetch_all(sql, params)
    return rows[0] if rows else None


def execute(sql, params=()):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        return cur.rowcount
    finally:
        conn.close()


def insert(sql, params=()):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()
```

`fetch_all` dan `execute` sama seperti minggu 3. Yang baru: `fetch_one` (ambil satu baris atau `None`) dan `insert` (mengembalikan `id` baris baru).

### C4 — Jalankan server dengan .env

Matikan server di Terminal 1 (`Ctrl+C`), lalu jalankan dengan cara baru.

**Terminal 1:**

```text
uv run --env-file .env fastapi dev main.py
```

Mulai sekarang server **selalu** dijalankan dengan `--env-file .env`.

### Titik cek C

- [ ] Server jalan tanpa error
- [ ] `git status` (di Terminal 2) tidak menampilkan `.env`, tapi menampilkan `.env.example`

**Dibahas trainer:**

- Environment variable dan kenapa rahasia tidak boleh ada di kode.
- `os.environ["X"]` (wajib ada, error kalau tidak ada) dibanding `os.environ.get("X", default)`.
- Nanti di minggu Docker, `.env` yang sama dipakai lagi.

---

## Bagian D — Membaca dari MySQL: GET (20 menit)

### D1 — Response task punya created_at

Tabel `tasks` di MySQL punya kolom `created_at` yang diisi otomatis. Tambahkan ke model `Task` di `schemas.py`.

Ubah baris import paling atas:

```python
from datetime import date, datetime
```

Lalu tambahkan satu field di paling bawah class `Task`:

```python
    created_at: datetime
```

### D2 — Ganti bagian atas routers/tasks.py

Buka `routers/tasks.py`. Ganti semua baris **dari paling atas sampai akhir fungsi `detail_task`** dengan isi di bawah ini. Fungsi POST, PUT, PATCH, DELETE di bawahnya **biarkan dulu**, nanti diganti di Bagian E.

**Isi file** (bagian atas):

```python
from fastapi import APIRouter, HTTPException, Query

from data import TASKS, id_berikutnya
from db import execute, fetch_all, fetch_one, insert
from schemas import Status, Task, TaskCreate, TaskUpdate

router = APIRouter(prefix="/v1/tasks", tags=["tasks"])

KOLOM = "id, project_id, title, status, priority, due_date, created_at"


def cari_task(task_id: int) -> dict:
    task = fetch_one(f"SELECT {KOLOM} FROM tasks WHERE id = %s", (task_id,))
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} tidak ditemukan")
    return task


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
```

Baris `from data import TASKS, id_berikutnya` sengaja masih ada, karena fungsi di bawahnya masih memakainya.

### D3 — Uji

**Terminal 2:**

```text
curl -s http://localhost:8000/v1/tasks | python3 -m json.tool
```

```text
curl -s "http://localhost:8000/v1/tasks?status=todo" | python3 -m json.tool
```

```text
curl -s "http://localhost:8000/v1/tasks?priority=1&limit=2" | python3 -m json.tool
```

```text
curl -i http://localhost:8000/v1/tasks/99
```

### Titik cek D

- [ ] Daftar task berisi 8 task dari MySQL (judulnya sama dengan hasil A3), lengkap dengan `created_at`
- [ ] `?status=todo` → task id 3, 5, 6, 8
- [ ] `?priority=1&limit=2` → task id 1 dan 2
- [ ] `/v1/tasks/99` → `404`

**Dibahas trainer:**

- Endpoint-nya sama persis dengan kemarin, yang berubah hanya cara mengambil data. Client tidak tahu dan tidak perlu tahu datanya dari mana.
- `WHERE` yang disusun sesuai filter yang dikirim. `%s` tetap dipakai untuk setiap nilai (ingat aturan minggu 3: jangan sambung teks SQL sendiri).
- `LIMIT` dan `OFFSET` di SQL menggantikan `hasil[offset : offset + limit]`.
- Satu request = buka koneksi, query, tutup koneksi. Cara yang lebih efisien (connection pool) dibahas belakangan.

---

## Bagian E — Menulis ke MySQL: POST, PATCH, PUT, DELETE (30 menit)

### E1 — POST (bersama trainer)

Ganti fungsi `buat_task` dengan:

```python
@router.post("", response_model=Task, status_code=201)
def buat_task(body: TaskCreate):
    pastikan_project_ada(body.project_id)
    id_baru = insert(
        "INSERT INTO tasks (project_id, title, status, priority, due_date) "
        "VALUES (%s, %s, %s, %s, %s)",
        (body.project_id, body.title, body.status, body.priority, body.due_date),
    )
    return cari_task(id_baru)
```

**Terminal 2:**

```text
curl -i -X POST http://localhost:8000/v1/tasks -H "Content-Type: application/json" -d '{"project_id": 2, "title": "Export rekap ke Excel", "priority": 1}'
```

Lalu **restart server** (simpan file apa saja, atau `Ctrl+C` dan jalankan lagi), dan panggil `GET /v1/tasks/9`. Task-nya masih ada.

### E2 — PATCH (bersama trainer)

Ganti fungsi `ubah_sebagian_task` dengan:

```python
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
```

**Terminal 2:**

```text
curl -s -X PATCH http://localhost:8000/v1/tasks/3 -H "Content-Type: application/json" -d '{"status": "doing", "priority": 1}' | python3 -m json.tool
```

```text
curl -i -X PATCH http://localhost:8000/v1/tasks/3 -H "Content-Type: application/json" -d '{"title": null}'
```

### E3 — PUT dan DELETE (kerjakan sendiri)

**PUT `ganti_task`:**

- Cari task dulu dengan `cari_task` (supaya `404` kalau tidak ada), lalu `pastikan_project_ada`
- `execute` sebuah `UPDATE tasks SET project_id = %s, title = %s, status = %s, priority = %s, due_date = %s WHERE id = %s`
- Kembalikan `cari_task(task_id)`

**DELETE `hapus_task`:**

- `execute` sebuah `DELETE FROM tasks WHERE id = %s`
- `execute` mengembalikan jumlah baris yang terhapus. Kalau `0`, kirim `404`
- Tidak perlu `cari_task` lebih dulu. Kenapa?

### E4 — Buang data di memori

Setelah keempat fungsi diganti, hapus baris ini di `routers/tasks.py`:

```python
from data import TASKS, id_berikutnya
```

`data.py` masih dipakai `routers/projects.py`, jadi jangan dihapus dulu. Itu urusan Bagian F.

### E5 — Uji

```text
curl -s -X PUT http://localhost:8000/v1/tasks/3 -H "Content-Type: application/json" -d '{"project_id": 1, "title": "Fitur keranjang belanja v2"}' | python3 -m json.tool
```

```text
curl -i -X DELETE http://localhost:8000/v1/tasks/8
```

```text
curl -i -X DELETE http://localhost:8000/v1/tasks/8
```

Cocokkan juga langsung di MySQL:

```text
mysql -u sakura_p00 -p sakura_db -e "SELECT id, title, status, priority, due_date FROM tasks"
```

### Titik cek E

- [ ] POST → `201`, task baru mendapat id 9 dan **masih ada setelah server restart**
- [ ] PATCH task 3 → status `doing`, priority `1`, field lain tidak berubah
- [ ] PATCH `{"title": null}` → `422` dengan `Field title tidak boleh null`
- [ ] PUT task 3 tanpa `status`, `priority`, `due_date` → kembali ke `todo`, `2`, `null`
- [ ] DELETE pertama `204`, DELETE kedua `404`
- [ ] Isi tabel di MySQL cocok dengan hasil curl
- [ ] `routers/tasks.py` tidak lagi memuat kata `TASKS`

**Dibahas trainer:**

- `insert` mengembalikan `lastrowid`, lalu task dibaca ulang dari database supaya `created_at` ikut terisi.
- Di PATCH, **nama kolom** disusun dengan f-string, tapi **nilai** tetap lewat `%s`. Kenapa nama kolom aman di sini? (Petunjuk: dari mana saja nama kolom bisa berasal kalau `extra="forbid"`?) Apa yang terjadi kalau nama kolom diambil langsung dari input client?
- Beda "tidak dikirim" dan "dikirim `null`" di PATCH, dan kenapa hanya `due_date` yang boleh `null` (cocokkan dengan `NULL` / `NOT NULL` di `schema.sql`).
- Kenapa DELETE cukup memeriksa `rowcount`.
- Foreign key di MySQL tetap menjadi penjaga terakhir kalau `pastikan_project_ada` terlewat.

---

## Bagian F — Project dari MySQL dan penanganan error (15 menit)

### F1 — Router project (kerjakan sendiri)

Ubah `routers/projects.py` supaya ketiga endpoint-nya memakai MySQL:

| Endpoint | Query |
| --- | --- |
| `GET /v1/projects` | `SELECT id, name, client FROM projects ORDER BY id` |
| `GET /v1/projects/{project_id}` | sama, dengan `WHERE id = %s`. `404` kalau `fetch_one` mengembalikan `None` |
| `GET /v1/projects/{project_id}/tasks` | `SELECT {KOLOM} FROM tasks WHERE project_id = %s ORDER BY id`. Ambil `KOLOM` dengan `from routers.tasks import KOLOM` |

Setelah selesai, hapus `from data import ...` dan hapus file `data.py`:

```text
rm data.py
```

### F2 — Kalau database mati (bersama trainer)

Coba matikan MySQL, lalu panggil API:

```text
sudo service mysql stop
```

```text
curl -i http://localhost:8000/v1/tasks
```

Muncul `500 Internal Server Error` dengan body teks biasa, dan Terminal 1 penuh tulisan merah. Client tidak tahu apa yang terjadi.

**File:** `main.py`, ganti seluruh isinya.

**Isi file:**

```python
import mysql.connector
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from routers import projects, tasks

app = FastAPI(title="Sakura Tasks API", version="0.2.0")


@app.exception_handler(mysql.connector.Error)
def database_bermasalah(request: Request, exc: mysql.connector.Error):
    print(f"[DB ERROR] {request.method} {request.url.path}: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Terjadi masalah di database. Coba lagi nanti."},
    )


@app.get("/")
def beranda():
    return {"pesan": "Sakura Tasks API jalan", "dokumentasi": "/docs"}


app.include_router(projects.router)
app.include_router(tasks.router)
```

Panggil lagi `curl -i http://localhost:8000/v1/tasks`, lalu nyalakan kembali MySQL:

```text
sudo service mysql start
```

### F3 — Tantangan (opsional)

Buat `GET /v1/projects/{project_id}/ringkasan` yang mengembalikan jumlah task per status:

```json
{"project_id": 1, "todo": 1, "doing": 1, "done": 1}
```

Petunjuk: `SELECT status, COUNT(*) AS jumlah FROM tasks WHERE project_id = %s GROUP BY status`. Status yang tidak punya task harus tetap muncul dengan nilai `0`.

### Titik cek F

- [ ] `GET /v1/projects` → 3 project dari MySQL
- [ ] `GET /v1/projects/2/tasks` → task milik project 2 dari MySQL
- [ ] `data.py` sudah tidak ada dan server tetap jalan
- [ ] Saat MySQL mati → `500` dengan body JSON `{"detail":"Terjadi masalah di database. Coba lagi nanti."}`, dan detail error tercetak di Terminal 1
- [ ] Setelah MySQL dinyalakan lagi, API normal kembali tanpa restart server

**Dibahas trainer:**

- Kenapa detail error (nama user, nama tabel, isi query) tidak boleh dikirim ke client. Ini bahan modul Security.
- `exception_handler`: satu tempat untuk menangani satu jenis error di seluruh aplikasi.
- `print` di sini hanya sementara. Logging yang benar dibahas di minggu testing dan debugging.

---

## Bagian G — Simpan ke Git dan GitHub (10 menit)

Matikan server di Terminal 1 dengan `Ctrl+C`.

**Ketik di terminal:**

```text
cd ~/seti-isd-materi
```

```text
git status
```

**Periksa dulu:** daftar file **tidak boleh** memuat `minggu-05-backend/sakura-api-p00/.env`. Kalau `.env` ada di daftar, berhenti dan ulangi C2.

**Ketik di terminal** (ganti `p00` dengan ID-mu):

```text
git add minggu-05-backend/sakura-api-p00
```

```text
git commit -m "Minggu 5 hari 2: validasi dan MySQL untuk Sakura Tasks API"
```

```text
git pull --rebase
```

```text
git push
```

### Titik cek G

- [ ] `git push` selesai tanpa error
- [ ] Di GitHub, folder `sakura-api-p00` memuat `db.py` dan `.env.example`, tapi **tidak** memuat `.env` dan `data.py`

---

## Titik cek akhir Hari 2 dan jika ada masalah

### Target minimal Hari 2

- [ ] Server jalan dengan `uv run --env-file .env fastapi dev main.py`
- [ ] Semua endpoint membaca dan menulis ke MySQL, data tetap ada setelah restart
- [ ] Data ngawur (judul pendek, priority di luar 1 sampai 3, tanggal lewat, field asing) ditolak dengan `422`
- [ ] Password MySQL tidak ada di kode dan tidak ada di GitHub
- [ ] Kamu bisa menjelaskan ke trainer: kenapa validasi harus di backend, kenapa nama kolom di PATCH aman disusun dengan f-string sedangkan nilainya tidak, dan apa gunanya `.env`

### Masalah yang sering muncul

| Pesan error | Penyebab | Yang dilakukan |
| --- | --- | --- |
| `KeyError: 'DB_USER'` saat server dinyalakan | Server dijalankan tanpa `--env-file .env`, atau `.env` tidak ada di folder `sakura-api-p00` | `uv run --env-file .env fastapi dev main.py` dari folder `sakura-api-p00` |
| `ModuleNotFoundError: No module named 'mysql'` | `mysql-connector-python` belum dipasang di proyek ini | `uv add mysql-connector-python` di folder `sakura-api-p00` |
| `500` dengan `Terjadi masalah di database` | Lihat baris `[DB ERROR]` di Terminal 1 | Biasanya salah satu dari tiga baris di bawah |
| `[DB ERROR] ... 2003 ... Can't connect to MySQL server` | MySQL belum menyala | `sudo service mysql start` |
| `[DB ERROR] ... 1045 ... Access denied` | User atau password di `.env` salah | Cek `DB_USER` sudah diganti ID-mu, `DB_PASSWORD` benar, tanpa spasi atau tanda kutip |
| `[DB ERROR] ... 1146 ... Table 'sakura_db.tasks' doesn't exist` | Tabel belum dibuat | Ulangi A2 |
| `ResponseValidationError` dan `created_at` disebut `Field required` | Query tidak memilih `created_at` | Pakai `KOLOM` di setiap `SELECT` task |
| `ImportError: cannot import name 'KOLOM'` | `KOLOM` belum dibuat di `routers/tasks.py` | Lihat D2 |
| `ModuleNotFoundError: No module named 'data'` setelah `rm data.py` | Masih ada `from data import ...` | Hapus baris itu di `routers/tasks.py` dan `routers/projects.py` |
| POST task baru dapat id 10, 11, bukan 9 | Pernah POST sebelumnya, atau ada POST yang gagal setelah id dipakai | Wajar, `AUTO_INCREMENT` tidak memakai ulang id. Kalau ingin sama dengan lembar, ulangi A2 |

### Jalur kejar

<details>
<summary>Kalau seed.sql tidak ada</summary>

**File (baru):** `~/seti-isd-materi/minggu-03-database/sakura-tasks-p00/db/seed.sql`

```sql
INSERT INTO projects (name, client) VALUES
  ('Toko Online Kopi Nusantara', 'Kopi Nusantara'),
  ('Aplikasi Absensi Sekolah', 'SD Harapan'),
  ('Sistem Antrean Klinik', 'Klinik Sehat');

INSERT INTO tasks (project_id, title, status, priority, due_date) VALUES
  (1, 'Desain halaman produk', 'done', 1, '2026-11-10'),
  (1, 'Integrasi pembayaran', 'doing', 1, '2026-11-20'),
  (1, 'Fitur keranjang belanja', 'todo', 2, '2026-11-25'),
  (2, 'Halaman login guru', 'done', 2, '2026-11-12'),
  (2, 'Rekap absensi bulanan', 'todo', 2, '2026-11-30'),
  (2, 'Notifikasi orang tua', 'todo', 3, NULL),
  (3, 'Nomor antrean otomatis', 'doing', 1, '2026-11-22'),
  (3, 'Layar panggilan pasien', 'todo', 2, '2026-12-05');
```

Lalu ulangi A2.

</details>

<details>
<summary>Jalur kejar: PUT dan DELETE (E3)</summary>

```python
@router.put("/{task_id}", response_model=Task)
def ganti_task(task_id: int, body: TaskCreate):
    cari_task(task_id)
    pastikan_project_ada(body.project_id)
    execute(
        "UPDATE tasks SET project_id = %s, title = %s, status = %s, "
        "priority = %s, due_date = %s WHERE id = %s",
        (body.project_id, body.title, body.status, body.priority, body.due_date, task_id),
    )
    return cari_task(task_id)


@router.delete("/{task_id}", status_code=204)
def hapus_task(task_id: int):
    jumlah = execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    if jumlah == 0:
        raise HTTPException(status_code=404, detail=f"Task {task_id} tidak ditemukan")
```

</details>

<details>
<summary>Jalur kejar: routers/projects.py (F1 dan F3)</summary>

Tambahkan juga model ini di `schemas.py` kalau mengerjakan F3:

```python
class RingkasanProject(BaseModel):
    project_id: int
    todo: int
    doing: int
    done: int
```

```python
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
```

</details>

<details>
<summary>Jalur kejar: semua file hasil akhir Hari 2</summary>

Isi lengkap semua file ada di folder `minggu-05-backend/referensi-hari-2/sakura-api-p00` di repo ini (dibagikan trainer setelah sesi). Selama sesi, pakai potongan-potongan di atas:

- `schemas.py`: B2, lalu tambahan `created_at` di D1
- `db.py`: C3
- `routers/tasks.py`: D2, E1, E2, lalu Jalur kejar PUT dan DELETE, tanpa baris `from data import ...`
- `routers/projects.py`: Jalur kejar F1 dan F3
- `main.py`: F2

</details>
