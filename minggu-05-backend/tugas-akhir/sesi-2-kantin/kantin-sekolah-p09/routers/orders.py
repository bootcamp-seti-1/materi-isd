from fastapi import APIRouter, HTTPException

import aturan
from db import execute, fetch_all, fetch_one, insert
from schemas import Laporan, Order, OrderCreate, StatusPesanan

router = APIRouter(prefix="/v1/orders", tags=["orders"])
laporan_router = APIRouter(prefix="/v1/laporan", tags=["laporan"])

KOLOM = "id, menu_id, qty, total, status, created_at"


def cari_order(order_id: int) -> dict:
    order = fetch_one(f"SELECT {KOLOM} FROM kantin_orders WHERE id = %s", (order_id,))
    if order is None:
        raise HTTPException(status_code=404, detail=f"Pesanan {order_id} tidak ditemukan")
    return order


@router.get("", response_model=list[Order])
def daftar_order(status: StatusPesanan | None = None):
    if status is not None:
        return fetch_all(
            f"SELECT {KOLOM} FROM kantin_orders WHERE status = %s ORDER BY id",
            (status,),
        )
    return fetch_all(f"SELECT {KOLOM} FROM kantin_orders ORDER BY id")


@router.get("/{order_id}", response_model=Order)
def detail_order(order_id: int):
    return cari_order(order_id)


@router.post("", response_model=Order, status_code=201)
def buat_order(body: OrderCreate):
    # 1. Menu tidak ada -> 400
    menu = fetch_one(
        "SELECT id, price, stock FROM kantin_menus WHERE id = %s",
        (body.menu_id,),
    )
    if menu is None:
        raise HTTPException(status_code=400, detail="Menu tidak ditemukan")

    # 2. Stok menu kurang dari qty -> 409
    if int(menu["stock"]) < body.qty:
        raise HTTPException(status_code=409, detail="Stok tidak cukup")

    # Hitung total & potongan diskon
    subtotal = int(menu["price"]) * body.qty
    if subtotal >= aturan.BATAS_DISKON:
        total = subtotal - (subtotal * aturan.DISKON_PERSEN // 100)
    else:
        total = subtotal

    # Kurangi stok menu & simpan pesanan baru
    execute(
        "UPDATE kantin_menus SET stock = stock - %s WHERE id = %s",
        (body.qty, body.menu_id),
    )
    id_baru = insert(
        "INSERT INTO kantin_orders (menu_id, qty, total, status) VALUES (%s, %s, %s, 'baru')",
        (body.menu_id, body.qty, total),
    )
    return cari_order(id_baru)


@router.post("/{order_id}/batal", response_model=Order)
def batal_order(order_id: int):
    # 1. Pesanan tidak ada -> 404
    order = cari_order(order_id)

    # 2. Pesanan sudah berstatus batal -> 409
    if order["status"] == "batal":
        raise HTTPException(status_code=409, detail="Pesanan sudah dibatalkan")

    # 3. Ubah status menjadi batal dan kembalikan stok menu
    execute(
        "UPDATE kantin_orders SET status = 'batal' WHERE id = %s",
        (order_id,),
    )
    execute(
        "UPDATE kantin_menus SET stock = stock + %s WHERE id = %s",
        (int(order["qty"]), int(order["menu_id"])),
    )
    return cari_order(order_id)


@laporan_router.get("", response_model=Laporan)
def laporan_penjualan():
    hasil = fetch_one(
        """
        SELECT
            COUNT(*) AS jumlah_pesanan,
            COALESCE(SUM(total), 0) AS pendapatan
        FROM kantin_orders
        WHERE status = 'baru'
        """
    )
    return {
        "jumlah_pesanan": int(hasil["jumlah_pesanan"]),
        "pendapatan": int(hasil["pendapatan"]),
    } 