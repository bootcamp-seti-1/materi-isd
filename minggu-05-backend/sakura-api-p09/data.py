# Daftar data awal (dummy) untuk project yang tersimpan di memori (RAM)
PROJECTS: list[dict] = [
    {"id": 1, "name": "Website Toko Sakura", "client": "CV Sakura"},
    {"id": 2, "name": "Aplikasi Kasir", "client": "Toko Melati"},
]

# Daftar data awal (dummy) untuk task yang tersimpan di memori (RAM)
TASKS: list[dict] = [
    {"id": 1, "project_id": 1, "title": "Desain halaman utama", "status": "done", "priority": 1, "due_date": None},
    {"id": 2, "project_id": 1, "title": "Integrasi keranjang", "status": "doing", "priority": 2, "due_date": "2026-05-01"},
    {"id": 3, "project_id": 1, "title": "Form pemesanan", "status": "todo", "priority": 2, "due_date": None},
    {"id": 4, "project_id": 2, "title": "Cetak struk", "status": "todo", "priority": 1, "due_date": "2026-04-20"},
    {"id": 5, "project_id": 2, "title": "Laporan harian", "status": "todo", "priority": 3, "due_date": None},
]


# Fungsi bantu untuk menghasilkan ID baru (mirip AUTO_INCREMENT di database).
# Mengambil ID terbesar di dalam list lalu ditambah 1; jika list kosong, mulai dari 1.
def id_berikutnya(daftar: list[dict]) -> int:
    return max((item["id"] for item in daftar), default=0) + 1 