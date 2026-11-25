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