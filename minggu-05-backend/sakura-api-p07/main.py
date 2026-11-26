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
