from fastapi import FastAPI

from routers import projects, tasks

# Menginisialisasi aplikasi utama FastAPI beserta judul dan versinya (tampil di /docs)
app = FastAPI(title="Sakura Tasks API", version="0.1.0")


# Endpoint root (/) untuk mengecek apakah server API sudah menyala dengan normal
@app.get("/")
def beranda():
    return {"pesan": "Sakura Tasks API jalan", "dokumentasi": "/docs"}


# Mendaftarkan seluruh endpoint dari file routers/projects.py ke aplikasi utama
app.include_router(projects.router)

# Mendaftarkan seluruh endpoint dari file routers/tasks.py ke aplikasi utama
app.include_router(tasks.router) 