"""Sudah jadi. Jangan diubah."""

import mysql.connector
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from routers import menus, orders

app = FastAPI(title="Kantin Sekolah API", version="0.1.0")


@app.exception_handler(mysql.connector.Error)
def database_bermasalah(request: Request, exc: mysql.connector.Error):
    print(f"[DB ERROR] {request.method} {request.url.path}: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Terjadi masalah di database. Coba lagi nanti."},
    )


@app.get("/")
def beranda():
    return {"pesan": "Kantin Sekolah API jalan", "dokumentasi": "/docs"}


app.include_router(menus.router)
app.include_router(orders.router)
app.include_router(orders.laporan_router)
