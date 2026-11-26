from fastapi import APIRouter, HTTPException

import aturan
from db import execute, fetch_all, fetch_one, insert  # noqa: F401
from schemas import Laporan, Order, OrderCreate, StatusPesanan

router = APIRouter(prefix="/v1/orders", tags=["orders"])
laporan_router = APIRouter(prefix="/v1/laporan", tags=["laporan"])

KOLOM = "id, menu_id, qty, total, status, created_at"


# ---------- TODO: kerjakan sesuai README ----------


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
    total = subtotal
    if subtotal >= aturan.BATAS_DISKON:
        total = subtotal * (100 - aturan.DISKON_PERSEN) // 100

    execute(
        "UPDATE kantin_menus SET stock = stock - %s WHERE id = %s",
        (body.qty, body.menu_id),
    )
    order_id = insert(
        "INSERT INTO kantin_orders (menu_id, qty, total, status) "
        "VALUES (%s, %s, %s, %s)",
        (body.menu_id, body.qty, total, "baru"),
    )

    order = fetch_one(
        f"SELECT {KOLOM} FROM kantin_orders WHERE id = %s",
        (order_id,),
    )
    if order is None:
        raise HTTPException(
            status_code=500,
            detail="Pesanan tersimpan tetapi tidak dapat dibaca",
        )
    return order


@router.get("/{order_id}", response_model=Order)
def detail_pesanan(order_id: int):
    order = fetch_one(
        f"SELECT {KOLOM} FROM kantin_orders WHERE id = %s",
        (order_id,),
    )
    if order is None:
        raise HTTPException(
            status_code=404,
            detail=f"Pesanan {order_id} tidak ditemukan",
        )
    return order


@router.post("/{order_id}/batal", response_model=Order)
def batalkan_pesanan(order_id: int):
    order = fetch_one(
        f"SELECT {KOLOM} FROM kantin_orders WHERE id = %s",
        (order_id,),
    )
    if order is None:
        raise HTTPException(
            status_code=404,
            detail=f"Pesanan {order_id} tidak ditemukan",
        )

    if order["status"] == "batal":
        raise HTTPException(status_code=409, detail="Pesanan sudah dibatalkan")

    execute(
        "UPDATE kantin_orders SET status = %s WHERE id = %s",
        ("batal", order_id),
    )
    execute(
        "UPDATE kantin_menus SET stock = stock + %s WHERE id = %s",
        (order["qty"], order["menu_id"]),
    )
    return detail_pesanan(order_id)


# ---------- Endpoint bonus ----------


@router.get("", response_model=list[Order])
def daftar_pesanan(status: StatusPesanan | None = None):
    if status is None:
        return fetch_all(f"SELECT {KOLOM} FROM kantin_orders ORDER BY id")

    return fetch_all(
        f"SELECT {KOLOM} FROM kantin_orders WHERE status = %s ORDER BY id",
        (status,),
    )


@laporan_router.get("", response_model=Laporan)
def laporan():
    hasil = fetch_one(
        "SELECT COUNT(*) AS jumlah_pesanan, "
        "COALESCE(SUM(total), 0) AS pendapatan "
        "FROM kantin_orders WHERE status = %s",
        ("baru",),
    )
    return Laporan(
        jumlah_pesanan=int(hasil["jumlah_pesanan"]),
        pendapatan=int(hasil["pendapatan"]),
    )
