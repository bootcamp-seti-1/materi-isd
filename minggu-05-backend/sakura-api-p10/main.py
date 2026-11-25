from fastapi import FastAPI

from routers import projects, tasks

app = FastAPI(title="Sakura Tasks API", version="0.1.0")


@app.get("/")
def beranda():
    return {"pesan": "Sakura Tasks API jalan", "dokumentasi": "/docs"}


app.include_router(projects.router)
app.include_router(tasks.router)