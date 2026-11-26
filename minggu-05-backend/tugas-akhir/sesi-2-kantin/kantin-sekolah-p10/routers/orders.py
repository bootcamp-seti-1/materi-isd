from fastapi import APIRouter, HTTPException

import aturan  # noqa: F401
from db import execute, fetch_all, fetch_one, insert  # noqa: F401
from schemas import Laporan, Order, OrderCreate, StatusPesanan

router = APIRouter(prefix="/v1/orders", tags=["orders"])
laporan_router = APIRouter(prefix="/v1/laporan", tags=["laporan"])

KOLOM = "id, menu_id, qty, total, status, created_at"


# ---------- TODO: kerjakan sesuai README ----------

def _ambil_pesanan(order_id: int) -> dict:
    pesanan = fetch_one(f"SELECT {KOLOM} FROM kantin_orders WHERE id = %s", (order_id,))
    if pesanan is None:
        raise HTTPException(status_code=404, detail=f"Pesanan {order_id} tidak ditemukan")
    return pesanan

@router.post("", response_model=Order, status_code=201)
def buat_pesanan(body: OrderCreate):

    menu = fetch_one(
        "SELECT id, price, stock FROM kantin_menus WHERE id = %s",
        (body.menu_id,),
    )

    if menu is None:
        raise HTTPException(status_code=400, detail="Menu tidak ditemukan")

    if menu["stock"] < body.qty:
        raise HTTPException(status_code=409, detail="Stok tidak cukup")

    subtotal = menu["price"] * body.qty
    total = subtotal * (100 - aturan.DISKON_PERSEN) // 100 if subtotal >= aturan.BATAS_DISKON else subtotal

    execute(
        "UPDATE kantin_menus SET stock = stock - %s WHERE id = %s",
        (body.qty, body.menu_id),
    )

    order_id = insert(
        "INSERT INTO kantin_orders (menu_id, qty, total, status) VALUES (%s, %s, %s, 'baru')",
        (body.menu_id, body.qty, total),
    )

    return _ambil_pesanan(order_id)



@router.get("/{order_id}", response_model=Order)
def detail_pesanan(order_id: int):
    return _ambil_pesanan(order_id)


@router.post("/{order_id}/batal", response_model=Order)
def batalkan_pesanan(order_id: int):
    pesanan = _ambil_pesanan(order_id)

    if pesanan["status"] == "batal":
        raise HTTPException(status_code=409, detail="Pesanan sudah dibatalkan")

    execute(
        "UPDATE kantin_orders SET status = 'batal' WHERE id = %s",
        (order_id,),
    )
    execute(
        "UPDATE kantin_menus SET stock = stock + %s WHERE id = %s",
        (pesanan["qty"], pesanan["menu_id"]),
    )
    return _ambil_pesanan(order_id)


# ---------- TODO bonus ----------


@router.get("", response_model=list[Order])
def daftar_pesanan(status: StatusPesanan | None = None):
    raise HTTPException(status_code=501, detail="Belum dibuat")


@laporan_router.get("", response_model=Laporan)
def laporan():
    raise HTTPException(status_code=501, detail="Belum dibuat")
