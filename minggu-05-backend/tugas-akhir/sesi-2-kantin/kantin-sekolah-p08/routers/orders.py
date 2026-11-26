from fastapi import APIRouter, HTTPException

import aturan  
from db import execute, fetch_all, fetch_one, get_connection, insert  
from schemas import Laporan, Order, OrderCreate, StatusPesanan

router = APIRouter(prefix="/v1/orders", tags=["orders"])
laporan_router = APIRouter(prefix="/v1/laporan", tags=["laporan"])

KOLOM = "id, menu_id, qty, total, status, created_at"


def cari_pesanan(order_id: int) -> dict:
    order = fetch_one(
        f"SELECT {KOLOM} FROM kantin_orders WHERE id = %s",
        (order_id,),
    )
    if order is None:
        raise HTTPException(status_code=404, detail=f"Pesanan {order_id} tidak ditemukan")
    return order

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

    stok_diperbarui = execute(
        "UPDATE kantin_menus SET stock = stock - %s "
        "WHERE id = %s AND stock >= %s",
        (body.qty, body.menu_id, body.qty),
    )
    if stok_diperbarui == 0:
        raise HTTPException(status_code=409, detail="Stok tidak cukup")

    order_id = insert(
        "INSERT INTO kantin_orders (menu_id, qty, total, status) "
        "VALUES (%s, %s, %s, %s)",
        (body.menu_id, body.qty, total, "baru"),
    )
    return cari_pesanan(order_id)

@router.get("/{order_id}", response_model=Order)
def detail_pesanan(order_id: int):
    return cari_pesanan(order_id)


@router.post("/{order_id}/batal", response_model=Order)
def batalkan_pesanan(order_id: int):
    order = cari_pesanan(order_id)
    if order["status"] == "batal":
        raise HTTPException(status_code=409, detail="Pesanan sudah dibatalkan")

    jumlah_diubah = execute(
        "UPDATE kantin_orders AS o "
        "JOIN kantin_menus AS m ON m.id = o.menu_id "
        "SET o.status = %s, m.stock = m.stock + o.qty "
        "WHERE o.id = %s AND o.status = %s",
        ("batal", order_id, "baru"),
    )
    if jumlah_diubah == 0:
        order = cari_pesanan(order_id)
        if order["status"] == "batal":
            raise HTTPException(status_code=409, detail="Pesanan sudah dibatalkan")

    return cari_pesanan(order_id)


# ---------- TODO bonus ----------


@router.get("", response_model=list[Order])
def daftar_pesanan(status: StatusPesanan | None = None):
    sql = f"SELECT {KOLOM} FROM kantin_orders"
    params = ()
    if status is not None:
        sql += " WHERE status = %s"
        params = (status,)
    sql += " ORDER BY id"
    return fetch_all(sql, params)


@laporan_router.get("", response_model=Laporan)
def laporan():
    return fetch_one(
        "SELECT COUNT(*) AS jumlah_pesanan, "
        "COALESCE(SUM(total), 0) AS pendapatan "
        "FROM kantin_orders WHERE status = %s",
        ("baru",),
    )
