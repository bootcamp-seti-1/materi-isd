# Hari 1 — Hands-on: Sakura Tasks API (HTTP, JSON, REST, FastAPI)

Ikuti langkahnya berurutan, ketik persis, dan cocokkan hasilmu di setiap titik cek. Penjelasan disampaikan trainer sambil mengetik.

Minggu lalu kamu membuat aplikasi menu Sakura Tasks yang berjalan di terminal. Minggu ini aplikasi itu dibuka ke dunia luar lewat **API**, supaya bisa dipakai oleh aplikasi lain: website, aplikasi HP, atau sistem klien. Hari ini datanya masih disimpan di memori. Besok (Hari 2) datanya disambungkan ke MySQL.

## Tujuan hari ini

Mas Bayu membuka rapat pagi:

> "Tim frontend minggu depan mulai bikin tampilan web Sakura Tasks. Mereka tidak boleh langsung masuk ke database kita. Mereka cuma boleh lewat API. Jadi minggu ini kita bikin API-nya. Hari ini kita sepakati dulu bentuk endpoint-nya, lalu langsung kita bangun dengan FastAPI."

### Hasil akhir yang dikejar hari ini

```text
minggu-05-backend/
  sakura-api-p00/
    main.py           titik masuk aplikasi
    data.py           data sementara (projects dan tasks)
    schemas.py        bentuk data yang masuk dan keluar
    routers/
      __init__.py     file kosong
      tasks.py        endpoint /v1/tasks
      projects.py     endpoint /v1/projects
```

Server dijalankan dengan:

```text
uv run fastapi dev main.py
```

Lalu API bisa dicoba dari browser di `http://localhost:8000/docs` dan dari terminal dengan `curl`.

## Persiapan sebelum mulai

- [✓] Laptop terhubung internet dan baterai aman untuk 2 jam
- [✓] Repo `seti-isd-materi` sudah ada di `~/seti-isd-materi` dan sudah `git pull`
- [✓] VS Code dan `uv` sudah terpasang (sama seperti minggu 3)
- [✓] Aku tahu ID pesertaku, ditulis huruf kecil (contoh: `p01`)

## Peta Hari 1 (120 menit)

| Bagian | Isi | Menit | Hasilnya |
| --- | --- | --- | --- |
| A | Persiapan proyek | 10 | Server FastAPI pertama jalan |
| B | Membedah HTTP dengan curl | 15 | Kamu bisa membaca request dan response |
| C | Desain API dulu, baru ngoding | 10 | Tabel endpoint Sakura Tasks |
| D | Membaca data: GET | 20 | Daftar task, filter, pagination, detail, 404 |
| E | Menambah data: POST | 15 | Task baru dengan status 201 |
| F | Mengubah dan menghapus: PUT, PATCH, DELETE | 25 | CRUD lengkap |
| G | Merapikan: router dan versi API | 15 | Struktur folder rapi, endpoint project |
| H | Simpan ke Git dan GitHub | 10 | Pekerjaan ter-push |

## Aturan main

1. Ikuti bagian dari A sampai H, berurutan.
2. Ketik hanya isi kotak berlabel **Ketik** atau **Isi file**. Sisanya dibaca saja.
3. Setiap bagian ditutup **Titik cek**. Cocok? Lanjut.
4. Tertinggal? Pakai **Jalur kejar** di bagian bawah, tidak perlu menunggu siapa pun.
5. Stuck? Tulis di grup: ID, bagian, dan tempel pesan error. Contoh: "P08 stuck di D3".
6. Boleh bertanya ke AI atau mencari di internet. Tapi kamu harus bisa menjelaskan sendiri apa yang kamu ketik.

## Cara membaca lembar ini

| Label | Artinya |
| --- | --- |
| **Folder** | Tempat kamu harus berada saat mengetik |
| **File** | Nama file beserta lokasinya. "Baru" berarti kamu yang membuatnya |
| **Isi file** | Teks yang ditempel ke dalam file di VS Code, lalu disimpan dengan `Ctrl+S` |
| **Ketik di terminal** | Perintah yang diketik di terminal |
| **Yang harus muncul di layar** | Hanya dibaca. Jangan diketik |
| **Titik cek** | Cocokkan hasilmu sebelum lanjut |
| **Dibahas trainer** | Poin yang dijelaskan trainer di bagian itu. Catat di sini kalau perlu |

Hari ini kamu memakai **dua terminal**:

- **Terminal 1 (server):** menjalankan `uv run fastapi dev main.py`. Biarkan terus menyala.
- **Terminal 2 (client):** mengetik perintah `curl`. Buka tab baru di aplikasi Ubuntu dengan `Ctrl+Shift+T`, atau buka terminal di VS Code dengan ``Ctrl+` ``.

### Kamus mini

| Kata | Artinya | Contoh |
| --- | --- | --- |
| API | Pintu yang dipakai program lain untuk memakai aplikasi kita | `GET /v1/tasks` |
| Endpoint | Satu alamat + satu method di API | `POST /v1/tasks` |
| Client | Yang mengirim request | browser, `curl`, aplikasi HP |
| Server | Yang menerima request dan mengirim response | FastAPI yang kamu jalankan |
| Resource | "Benda" yang dikelola API, ditulis sebagai kata benda jamak | `tasks`, `projects` |
| Path parameter | Bagian alamat yang berubah-ubah | `5` di `/v1/tasks/5` |
| Query parameter | Pilihan tambahan setelah tanda `?` | `?status=todo&limit=5` |
| Body | Isi data yang dikirim bersama request | `{"title": "Cetak struk"}` |
| Status code | Angka 3 digit di response yang menyatakan hasilnya | `200`, `201`, `404` |

---

## Bagian A — Persiapan proyek (10 menit)

### A1 — Masuk ke folder repo dan ambil materi terbaru

**Ketik di terminal:**

```text
cd ~/seti-isd-materi
```

```text
git pull --rebase
```

### A2 — Buat proyek baru

**Ketik di terminal** (ganti `p00` dengan ID-mu):

```text
mkdir -p minggu-05-backend
```

```text
cd minggu-05-backend
```

```text
uv init --no-package sakura-api-p00
```

```text
cd sakura-api-p00
```

### A3 — Pasang FastAPI

**Folder:** `sakura-api-p00`

**Ketik di terminal:**

```text
uv add "fastapi[standard]"
```

Tanda kutip wajib. Tanpa tanda kutip, terminal salah membaca tanda kurung siku.

### A4 — Endpoint pertama

**Ketik di terminal:**

```text
code .
```

`uv init` sudah membuat `main.py` berisi contoh `print("Hello...")`. Hapus semua isinya, lalu ganti.

**File:** `main.py`

**Isi file:**

```python
from fastapi import FastAPI

app = FastAPI(title="Sakura Tasks API", version="0.1.0")


@app.get("/")
def beranda():
    return {"pesan": "Sakura Tasks API jalan", "dokumentasi": "/docs"}
```

### A5 — Jalankan server

**Terminal 1, folder:** `sakura-api-p00`

```text
uv run fastapi dev main.py
```

**Yang harus muncul di layar** (kurang lebih):

```text
INFO     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO     Application startup complete.
```

Buka browser di Windows, lalu masuk ke:

- `http://localhost:8000` → muncul `{"pesan":"Sakura Tasks API jalan","dokumentasi":"/docs"}`
- `http://localhost:8000/docs` → muncul halaman dokumentasi API (Swagger UI)

Mode `dev` otomatis me-restart server setiap kali file disimpan. Kamu tidak perlu mematikan dan menyalakan ulang.

### Titik cek A

- [✓] `http://localhost:8000` menampilkan pesan JSON
- [✓] `http://localhost:8000/docs` terbuka

**Dibahas trainer:** apa itu API dan kenapa frontend tidak boleh langsung ke database; apa itu framework; kenapa FastAPI.

---

## Bagian B — Membedah HTTP dengan curl (15 menit)

Browser menyembunyikan banyak hal. `curl` memperlihatkan semuanya.

### B1 — Lihat request dan response lengkap

**Terminal 2:**

```text
curl -v http://localhost:8000/
```

**Yang harus muncul di layar** (dipotong):

```text
> GET / HTTP/1.1
> Host: localhost:8000
> User-Agent: curl/8.5.0
> Accept: */*
>
< HTTP/1.1 200 OK
< date: Mon, 23 Nov 2026 01:00:00 GMT
< server: uvicorn
< content-length: 58
< content-type: application/json
<
{"pesan":"Sakura Tasks API jalan","dokumentasi":"/docs"}
```

Baris yang diawali `>` adalah **request** (dikirim curl). Baris yang diawali `<` adalah **response** (dikirim server). Tuliskan di bawah ini, lalu cocokkan dengan trainer:

| Pertanyaan | Jawabanmu |
| --- | --- |
| Method apa yang dipakai? | GET |
| Path apa yang diminta? | / |
| Status code berapa? | 200 |
| Header apa yang menyatakan isi response berbentuk JSON? | content-length: 58 content-type: application/json |

### B2 — Minta alamat yang tidak ada

```text
curl -i http://localhost:8000/tidak-ada
```

`-i` hanya menampilkan response (tanpa request). Perhatikan status code-nya.

### B3 — Pakai method yang salah

```text
curl -i -X DELETE http://localhost:8000/
```

`-X` memilih method. Endpoint `/` hanya menerima `GET`, jadi server menolak.

### Titik cek B

- [✓] B1 menunjukkan `200 OK` dan `content-type: application/json`
- [✓] B2 menunjukkan `404 Not Found`
- [✓] B3 menunjukkan `405 Method Not Allowed`

**Dibahas trainer:**

- Struktur request: method, path, header, body. Struktur response: status code, header, body.
- Method: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`. Mana yang aman (tidak mengubah data) dan mana yang idempoten (diulang berkali-kali hasilnya sama).
- Kelas status code: 2xx berhasil, 3xx dialihkan, 4xx salah di client, 5xx salah di server.
- Header penting: `Content-Type`, `Accept`, `Authorization` (dipakai di modul Security).
- JSON: tipe datanya (string, number, boolean, null, array, object) dan bedanya dengan dict Python.

---

## Bagian C — Desain API dulu, baru ngoding (10 menit)

Di industri, bentuk API disepakati dulu dengan tim frontend sebelum ditulis kodenya. Isi kolom yang kosong (`?`) di tabel ini. Kerjakan di kertas atau langsung di file ini.

| No | Method | Path | Kegunaan | Status kalau berhasil |
| --- | --- | --- | --- | --- |
| 1 | `GET` | `/v1/tasks` | Daftar task (bisa difilter) | `200` |
| 2 | `GET` | `/v1/tasks/{task_id}` | Detail satu task | `200` |
| 3 | `POST` | `/v1/tasks` | Membuat task baru | `200` |
| 4 | `PUT` | `/v1/tasks/{task_id}` | Mengganti seluruh isi satu task | `200` |
| 5 | `PATCH` | `/v1/tasks/{task_id}` | Mengubah sebagian isi task, misalnya status saja | `200` |
| 6 | `DELETE` | `/v1/tasks/{task_id}` | Menghapus task | `204` |
| 7 | `GET` | `/v1/projects` | Daftar project | `200` |
| 8 | `GET` | `GET` | Semua task milik satu project | `200` |

Kalau task yang diminta tidak ada, status code-nya `404 Not Found`.

<details>
<summary>Kunci (buka setelah dibahas)</summary>

3: `POST`, `201` · 4: `/v1/tasks/{task_id}` · 5: `PATCH` · 6: `204` · 8: `/v1/projects/{project_id}/tasks` · tidak ada: `404`

</details>

Contoh **filter dan pagination** lewat query parameter:

```text
GET /v1/tasks?status=todo               task yang statusnya todo
GET /v1/tasks?priority=1                task prioritas 1
GET /v1/tasks?limit=2&offset=2          2 task, mulai dari urutan ke-3
```

### Titik cek C

- [✓] Semua `?` di tabel sudah terisi dan cocok dengan kunci

**Dibahas trainer:**

- Aturan REST: alamat berisi kata benda (resource) jamak, aksinya ditentukan method. Bandingkan `POST /v1/tasks` dengan `/buatTask` atau `/getAllTasks`.
- Nested resource: `/v1/projects/1/tasks`.
- Filter, sort, pagination lewat query parameter, bukan alamat baru.
- Versi API (`/v1`): kenapa perlu, dan apa yang terjadi kalau tidak ada.
- Format error yang seragam supaya frontend mudah membacanya.

---

## Bagian D — Membaca data: GET (20 menit)

### D1 — Data sementara

Datanya sengaja dibuat sama bentuknya dengan tabel `projects` dan `tasks` di minggu 3.

**File (baru):** `data.py`

**Isi file:**

```python
from datetime import date

PROJECTS = [
    {"id": 1, "name": "Website Toko Kue", "client": "Toko Kue Bu Sari"},
    {"id": 2, "name": "Aplikasi Kasir", "client": "Warung Pak Darto"},
    {"id": 3, "name": "Sistem Absensi", "client": "SD Harapan"},
]

TASKS = [
    {"id": 1, "project_id": 1, "title": "Desain halaman utama", "status": "done", "priority": 1, "due_date": date(2026, 11, 20)},
    {"id": 2, "project_id": 1, "title": "Halaman daftar kue", "status": "doing", "priority": 1, "due_date": date(2026, 11, 27)},
    {"id": 3, "project_id": 1, "title": "Form pemesanan", "status": "todo", "priority": 2, "due_date": None},
    {"id": 4, "project_id": 2, "title": "Hitung kembalian", "status": "todo", "priority": 1, "due_date": date(2026, 11, 30)},
    {"id": 5, "project_id": 2, "title": "Cetak struk", "status": "todo", "priority": 3, "due_date": None},
    {"id": 6, "project_id": 3, "title": "Rancang tabel absensi", "status": "doing", "priority": 2, "due_date": date(2026, 12, 4)},
]


def id_berikutnya(rows):
    return max((r["id"] for r in rows), default=0) + 1
```

### D2 — Daftar task

**File:** `main.py`, ganti seluruh isinya.

**Isi file:**

```python
from fastapi import FastAPI, HTTPException

from data import TASKS

app = FastAPI(title="Sakura Tasks API", version="0.1.0")


@app.get("/")
def beranda():
    return {"pesan": "Sakura Tasks API jalan", "dokumentasi": "/docs"}


@app.get("/v1/tasks")
def daftar_task():
    return TASKS
```

**Terminal 2:**

```text
curl -s http://localhost:8000/v1/tasks | python3 -m json.tool
```

`-s` menyembunyikan progres curl. `python3 -m json.tool` merapikan JSON supaya mudah dibaca. Perhatikan: `date(2026, 11, 20)` di Python otomatis menjadi teks `"2026-11-20"` di JSON.

### D3 — Filter dan pagination

Ubah fungsi `daftar_task` di `main.py`. Ganti juga baris import FastAPI.

**Isi file** (bagian yang berubah):

```python
from fastapi import FastAPI, HTTPException, Query
```

```python
@app.get("/v1/tasks")
def daftar_task(
    status: str | None = None,
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
```

**Terminal 2**, coba satu per satu:

```text
curl -s "http://localhost:8000/v1/tasks?status=todo" | python3 -m json.tool
```

```text
curl -s "http://localhost:8000/v1/tasks?limit=2&offset=2" | python3 -m json.tool
```

```text
curl -i "http://localhost:8000/v1/tasks?limit=500"
```

Alamat yang berisi `?` dan `&` wajib diberi tanda kutip. Tanpa tanda kutip, terminal menganggap `&` sebagai perintah lain.

### D4 — Detail task dan 404

Tambahkan di bawah `daftar_task`:

```python
def cari_task(task_id: int) -> dict:
    for t in TASKS:
        if t["id"] == task_id:
            return t
    raise HTTPException(status_code=404, detail=f"Task {task_id} tidak ditemukan")


@app.get("/v1/tasks/{task_id}")
def detail_task(task_id: int):
    return cari_task(task_id)
```

**Terminal 2:**

```text
curl -i http://localhost:8000/v1/tasks/2
```

```text
curl -i http://localhost:8000/v1/tasks/99
```

```text
curl -i http://localhost:8000/v1/tasks/abc
```

### Titik cek D

- [✓] `?status=todo` hanya mengembalikan 3 task (id 3, 4, 5)
- [✓] `?limit=2&offset=2` mengembalikan task id 3 dan 4
- [✓] `?limit=500` ditolak dengan `422`
- [✓] `/v1/tasks/99` → `404` dengan `{"detail":"Task 99 tidak ditemukan"}`
- [✓] `/v1/tasks/abc` → `422`, karena `task_id` harus angka

**Dibahas trainer:**

- Path parameter dan query parameter, dan bagaimana FastAPI membacanya dari parameter fungsi.
- Type hint (`int`, `str | None`) dipakai FastAPI untuk mengubah dan memeriksa input. Itu sebabnya `abc` ditolak tanpa kita menulis `if`.
- Beda `404` (datanya tidak ada) dengan `422` (format inputnya salah).
- `HTTPException` menghentikan fungsi dan langsung mengirim response error.
- Coba endpoint yang sama dari `/docs` dengan tombol **Try it out**.

---

## Bagian E — Menambah data: POST (15 menit)

### E1 — Bentuk data yang boleh dikirim

**File (baru):** `schemas.py`

**Isi file:**

```python
from datetime import date
from typing import Literal

from pydantic import BaseModel

Status = Literal["todo", "doing", "done"]


class TaskCreate(BaseModel):
    project_id: int
    title: str
    status: Status = "todo"
    priority: int = 2
    due_date: date | None = None


class Task(TaskCreate):
    id: int
```

### E2 — Endpoint POST

Di `main.py`, ubah baris import dan tambahkan endpoint baru di paling bawah.

**Isi file** (bagian yang berubah):

```python
from data import PROJECTS, TASKS, id_berikutnya
from schemas import Task, TaskCreate
```

```python
def pastikan_project_ada(project_id: int) -> None:
    if not any(p["id"] == project_id for p in PROJECTS):
        raise HTTPException(status_code=400, detail=f"Project {project_id} tidak ada")


@app.post("/v1/tasks", response_model=Task, status_code=201)
def buat_task(body: TaskCreate):
    pastikan_project_ada(body.project_id)
    task_baru = {"id": id_berikutnya(TASKS), **body.model_dump()}
    TASKS.append(task_baru)
    return task_baru
```

### E3 — Kirim data dengan curl

**Terminal 2:**

```text
curl -i -X POST http://localhost:8000/v1/tasks -H "Content-Type: application/json" -d '{"project_id": 2, "title": "Laporan harian", "priority": 1}'
```

**Yang harus muncul di layar** (bagian akhir):

```text
HTTP/1.1 201 Created
...
{"project_id":2,"title":"Laporan harian","status":"todo","priority":1,"due_date":null,"id":7}
```

`-H` menambahkan header, `-d` mengirim body. Perhatikan `status` dan `due_date` terisi otomatis dari nilai default.

Sekarang coba kirim data yang salah, satu per satu, lalu baca pesan errornya:

```text
curl -i -X POST http://localhost:8000/v1/tasks -H "Content-Type: application/json" -d '{"project_id": 2}'
```

```text
curl -i -X POST http://localhost:8000/v1/tasks -H "Content-Type: application/json" -d '{"project_id": 2, "title": "Uji", "status": "selesai"}'
```

```text
curl -i -X POST http://localhost:8000/v1/tasks -H "Content-Type: application/json" -d '{"project_id": 99, "title": "Uji"}'
```

### Titik cek E

- [✓] Task baru dibuat dengan `201 Created` dan mendapat `id` 7
- [✓] `GET /v1/tasks/7` menampilkan task itu
- [✓] Body tanpa `title` → `422`, pesannya menyebut `title` dan `Field required`
- [✓] `status` selain `todo`/`doing`/`done` → `422`
- [✓] `project_id` 99 → `400` dengan `Project 99 tidak ada`

**Dibahas trainer:**

- Pydantic `BaseModel`: satu class sekaligus menjadi aturan, pengubah tipe, dan dokumentasi (lihat bagian **Schemas** di `/docs`).
- `Literal` untuk nilai yang pilihannya terbatas, sama seperti `ENUM` di MySQL.
- `response_model`: hanya field di model yang dikirim balik ke client.
- Kenapa `201` dan bukan `200`.
- Restart server lalu `GET /v1/tasks`: task nomor 7 hilang. Kenapa? (Jawabannya: data di memori. Besok diselesaikan dengan MySQL.)

---

## Bagian F — Mengubah dan menghapus: PUT, PATCH, DELETE (25 menit)

Bagian ini dikerjakan **sendiri**. Petunjuknya ada, kodenya tidak. Kalau sudah lewat 20 menit dan belum jalan, buka Jalur kejar.

### F1 — PUT: mengganti seluruh isi task

- Path: `/v1/tasks/{task_id}`, body: `TaskCreate` (semua field wajib, sama seperti POST)
- Cari task dengan `cari_task`. Periksa project dengan `pastikan_project_ada`.
- Timpa isi task: `task.update(body.model_dump())`
- Kembalikan task, `response_model=Task`

### F2 — PATCH: mengubah sebagian

Tambahkan model baru di `schemas.py`. Semua field boleh tidak dikirim:

```python
class TaskUpdate(BaseModel):
    project_id: int | None = None
    title: str | None = None
    status: Status | None = None
    priority: int | None = None
    due_date: date | None = None
```

- Path: `/v1/tasks/{task_id}`, body: `TaskUpdate`
- Ambil hanya field yang benar-benar dikirim client: `body.model_dump(exclude_unset=True)`
- Kalau `project_id` ikut dikirim, periksa dulu dengan `pastikan_project_ada`
- Perbarui task dengan hasil di atas, lalu kembalikan

### F3 — DELETE: menghapus

- Path: `/v1/tasks/{task_id}`, `status_code=204`
- Cari task, lalu `TASKS.remove(task)`. Fungsi tidak perlu mengembalikan apa-apa.

### F4 — Uji

```text
curl -i -X PATCH http://localhost:8000/v1/tasks/3 -H "Content-Type: application/json" -d '{"status": "doing"}'
```

```text
curl -i -X PUT http://localhost:8000/v1/tasks/3 -H "Content-Type: application/json" -d '{"project_id": 1, "title": "Form pemesanan online"}'
```

```text
curl -i -X DELETE http://localhost:8000/v1/tasks/5
```

```text
curl -i -X DELETE http://localhost:8000/v1/tasks/5
```

### Titik cek F

- [✓] PATCH mengubah status task 3 menjadi `doing`, field lain tetap
- [✓] PUT task 3 tanpa `priority` dan `status` membuat keduanya kembali ke default (`2` dan `todo`)
- [✓] DELETE pertama → `204 No Content`, DELETE kedua → `404`
- [✓] Semua endpoint muncul di `/docs`

**Dibahas trainer:**

- Beda PUT (ganti semua, field yang tidak dikirim kembali ke default) dan PATCH (ganti yang dikirim saja). Buktikan dengan hasil F4.
- `exclude_unset=True`: beda "tidak dikirim" dengan "dikirim `null`".
- Kenapa `204` tidak punya body.
- Idempoten: DELETE dua kali hasilnya beda status code, tapi keadaan datanya sama.

---

## Bagian G — Merapikan: router dan versi API (15 menit)

`main.py` sudah panjang. Kalau nanti ada 10 resource, semuanya akan tercampur. Endpoint dipisah per resource dengan `APIRouter`.

### G1 — Pindahkan endpoint task

**Ketik di terminal:**

```text
mkdir routers
```

```text
touch routers/__init__.py
```

**File (baru):** `routers/tasks.py`

Pindahkan **semua** endpoint dan fungsi bantu task dari `main.py` ke file ini, lalu lakukan tiga perubahan:

1. Bagian atas file:

```python
from fastapi import APIRouter, HTTPException, Query

from data import PROJECTS, TASKS, id_berikutnya
from schemas import Status, Task, TaskCreate, TaskUpdate

router = APIRouter(prefix="/v1/tasks", tags=["tasks"])
```

2. Ganti `@app.` menjadi `@router.` di semua endpoint.
3. Hapus `/v1/tasks` dari path, karena sudah ditulis di `prefix`:
   - `@app.get("/v1/tasks")` → `@router.get("")`
   - `@app.get("/v1/tasks/{task_id}")` → `@router.get("/{task_id}")`
   - lakukan hal yang sama untuk POST, PUT, PATCH, DELETE

Sekalian, ganti tipe `status` di `daftar_task` dari `str | None` menjadi `Status | None`, supaya filter dengan status yang salah juga ditolak.

### G2 — main.py jadi ringkas

**File:** `main.py`, ganti seluruh isinya.

**Isi file:**

```python
from fastapi import FastAPI

from routers import projects, tasks

app = FastAPI(title="Sakura Tasks API", version="0.1.0")


@app.get("/")
def beranda():
    return {"pesan": "Sakura Tasks API jalan", "dokumentasi": "/docs"}


app.include_router(projects.router)
app.include_router(tasks.router)
```

### G3 — Router project (kerjakan sendiri)

Tambahkan model di `schemas.py`:

```python
class Project(BaseModel):
    id: int
    name: str
    client: str
```

**File (baru):** `routers/projects.py`, dengan `prefix="/v1/projects"` dan `tags=["projects"]`. Buat tiga endpoint:

| Endpoint | Isi |
| --- | --- |
| `GET ""` | semua project, `response_model=list[Project]` |
| `GET "/{project_id}"` | satu project, `404` kalau tidak ada |
| `GET "/{project_id}/tasks"` | task milik project itu, `404` kalau project tidak ada |

### Titik cek G

- [✓] Server jalan lagi tanpa error setelah `main.py` diganti
- [✓] Di `/docs`, endpoint terkelompok menjadi **projects** dan **tasks**
- [✓] `curl -s http://localhost:8000/v1/projects/1/tasks | python3 -m json.tool` mengembalikan task milik project 1
- [✓] `curl -i http://localhost:8000/v1/projects/99/tasks` → `404`
- [✓] `curl -i "http://localhost:8000/v1/tasks?status=selesai"` → `422`

**Dibahas trainer:**

- Kenapa kode dipisah per resource (dibahas lebih dalam di minggu arsitektur).
- `prefix` dan `tags`.
- Kalau nanti ada `/v2`, `/v1` tetap jalan untuk aplikasi lama.

---

## Bagian H — Simpan ke Git dan GitHub (10 menit)

Matikan server di Terminal 1 dengan `Ctrl+C`.

**Ketik di terminal:**

```text
cd ~/seti-isd-materi
```

**Ketik di terminal** (ganti `p00` dengan ID-mu):

```text
git add minggu-05-backend/sakura-api-p00
```

```text
git commit -m "Minggu 5 hari 1: Sakura Tasks API (CRUD in-memory, router)"
```

```text
git pull --rebase
```

```text
git push
```

Kalau `git push` ditolak dengan tulisan `rejected` atau `fetch first`, ulangi `git pull --rebase`, lalu `git push`.

Pastikan folder `.venv` **tidak** ikut ter-push. File `.gitignore` buatan `uv init` sudah mengecualikannya.

### Titik cek H

- [ ] `git push` selesai tanpa error
- [ ] Di GitHub, folder `minggu-05-backend/sakura-api-p00` berisi `main.py`, `data.py`, `schemas.py`, dan folder `routers`

---

## Titik cek akhir Hari 1 dan jika ada masalah

### Target minimal Hari 1

- [✓] Server jalan dengan `uv run fastapi dev main.py`
- [✓] Ke-8 endpoint di tabel Bagian C bekerja dan muncul di `/docs`
- [✓] Kamu bisa membaca output `curl -v`: mana request, mana response, berapa status code-nya
- [✓] Kamu bisa menjelaskan ke trainer: beda `404` dan `422`, beda PUT dan PATCH, kenapa POST mengembalikan `201`
- [✓] Pekerjaanmu sudah di-push dan terlihat di GitHub

### Masalah yang sering muncul

| Pesan error | Penyebab | Yang dilakukan |
| --- | --- | --- |
| `uv add` gagal dengan pesan aneh soal `fastapi[standard]` | Tanda kutip lupa | `uv add "fastapi[standard]"` |
| `Failed to connect to localhost port 8000` | Server di Terminal 1 belum jalan atau sudah mati | Jalankan lagi `uv run fastapi dev main.py` di folder `sakura-api-p00` |
| `[Errno 98] Address already in use` | Masih ada server lain di port 8000 | Tutup terminal lama, atau jalankan `uv run fastapi dev main.py --port 8001` |
| `ModuleNotFoundError: No module named 'data'` | Server dijalankan dari folder yang salah | `cd ~/seti-isd-materi/minggu-05-backend/sakura-api-p00` |
| `ModuleNotFoundError: No module named 'routers'` | `routers/__init__.py` belum dibuat | `touch routers/__init__.py` |
| `ImportError: cannot import name 'TaskUpdate'` | Model belum ditambahkan di `schemas.py` | Tambahkan class `TaskUpdate` (F2) |
| `422` dengan `"type":"json_invalid"` | Body curl bukan JSON yang benar: kutip tunggal di dalam, koma kurang, atau body dibungkus kutip dua | Body di dalam `'...'`, kunci dan teks di dalam `"..."` |
| `422` padahal datanya benar | Header `Content-Type: application/json` lupa | Tambahkan `-H "Content-Type: application/json"` |
| `405 Method Not Allowed` | Method atau path tidak cocok dengan endpoint | Cek `-X` dan path, bandingkan dengan `/docs` |
| `http://localhost:8000` tidak terbuka di browser Windows | Server mendengarkan di WSL, browser di Windows | Coba `http://127.0.0.1:8000`. Kalau masih gagal, jalankan `uv run fastapi dev main.py --host 0.0.0.0` |

### Jalur kejar

Kalau tertinggal lebih dari satu bagian, buat semua file di bawah ini persis, lalu lanjut dari bagian yang sedang dikerjakan kelas.

<details>
<summary>Jalur kejar: semua file hasil akhir Hari 1</summary>

**Ketik di terminal:**

```text
cd ~/seti-isd-materi/minggu-05-backend/sakura-api-p00
```

```text
mkdir -p routers && touch routers/__init__.py
```

`data.py`: sama persis dengan D1.

**`schemas.py`**

```python
from datetime import date
from typing import Literal

from pydantic import BaseModel

Status = Literal["todo", "doing", "done"]


class TaskCreate(BaseModel):
    project_id: int
    title: str
    status: Status = "todo"
    priority: int = 2
    due_date: date | None = None


class TaskUpdate(BaseModel):
    project_id: int | None = None
    title: str | None = None
    status: Status | None = None
    priority: int | None = None
    due_date: date | None = None


class Task(TaskCreate):
    id: int


class Project(BaseModel):
    id: int
    name: str
    client: str
```

**`routers/tasks.py`**

```python
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
```

**`routers/projects.py`**

```python
from fastapi import APIRouter, HTTPException

from data import PROJECTS, TASKS
from schemas import Project, Task

router = APIRouter(prefix="/v1/projects", tags=["projects"])


def cari_project(project_id: int) -> dict:
    for p in PROJECTS:
        if p["id"] == project_id:
            return p
    raise HTTPException(status_code=404, detail=f"Project {project_id} tidak ditemukan")


@router.get("", response_model=list[Project])
def daftar_project():
    return PROJECTS


@router.get("/{project_id}", response_model=Project)
def detail_project(project_id: int):
    return cari_project(project_id)


@router.get("/{project_id}/tasks", response_model=list[Task])
def task_milik_project(project_id: int):
    cari_project(project_id)
    return [t for t in TASKS if t["project_id"] == project_id]
```

`main.py`: sama persis dengan G2.

</details>

<details>
<summary>Jalur kejar: kalau baru selesai Bagian E dan stuck di F (PUT, PATCH, DELETE saja)</summary>

Tempel di bawah `buat_task` di `main.py`, dan tambahkan `TaskUpdate` (F2) ke `schemas.py` serta ke baris `from schemas import ...`.

```python
@app.put("/v1/tasks/{task_id}", response_model=Task)
def ganti_task(task_id: int, body: TaskCreate):
    task = cari_task(task_id)
    pastikan_project_ada(body.project_id)
    task.update(body.model_dump())
    return task


@app.patch("/v1/tasks/{task_id}", response_model=Task)
def ubah_sebagian_task(task_id: int, body: TaskUpdate):
    task = cari_task(task_id)
    perubahan = body.model_dump(exclude_unset=True)
    if "project_id" in perubahan:
        pastikan_project_ada(perubahan["project_id"])
    task.update(perubahan)
    return task


@app.delete("/v1/tasks/{task_id}", status_code=204)
def hapus_task(task_id: int):
    task = cari_task(task_id)
    TASKS.remove(task)
```

</details>
