from fastapi import APIRouter, HTTPException

import aturan  # noqa: F401
from db import execute, fetch_all, fetch_one, insert  # noqa: F401
from schemas import Laporan, Order, OrderCreate, StatusPesanan

router = APIRouter(prefix="/v1/orders", tags=["orders"])
laporan_router = APIRouter(prefix="/v1/laporan", tags=["laporan"])

KOLOM = "id, menu_id, qty, total, status, created_at"


# ---------- TODO: kerjakan sesuai README ----------


@router.post("", response_model=Order, status_code=201)
def buat_pesanan(body: OrderCreate):
    raise HTTPException(status_code=501, detail="Belum dibuat")


@router.get("/{order_id}", response_model=Order)
def detail_pesanan(order_id: int):
    raise HTTPException(status_code=501, detail="Belum dibuat")


@router.post("/{order_id}/batal", response_model=Order)
def batalkan_pesanan(order_id: int):
    raise HTTPException(status_code=501, detail="Belum dibuat")


# ---------- TODO bonus ----------


@router.get("", response_model=list[Order])
def daftar_pesanan(status: StatusPesanan | None = None):
    raise HTTPException(status_code=501, detail="Belum dibuat")


@laporan_router.get("", response_model=Laporan)
def laporan():
    raise HTTPException(status_code=501, detail="Belum dibuat")
