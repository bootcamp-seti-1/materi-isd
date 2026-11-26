from contextlib import contextmanager

from fastapi import APIRouter, HTTPException

import aturan
from db import fetch_all, fetch_one, get_connection
from schemas import Laporan, Order, OrderCreate, StatusPesanan

router = APIRouter(prefix="/v1/orders", tags=["orders"])
laporan_router = APIRouter(prefix="/v1/laporan", tags=["laporan"])

KOLOM = "id, menu_id, qty, total, status, created_at"


@contextmanager
def transaksi_pesanan():
    """Simpan perubahan stok dan pesanan dalam satu transaksi."""
    with get_connection() as conn, conn.cursor(dictionary=True) as cur:
        conn.start_transaction()
        try:
            yield cur
            conn.commit()
        except Exception:
            conn.rollback()
            raise


@router.post("", response_model=Order, status_code=201)
def buat_pesanan(body: OrderCreate):
    with transaksi_pesanan() as cur:
        # Kunci baris sampai transaksi selesai agar pemesan lain membaca stok terbaru.
        cur.execute(
            "SELECT price, stock FROM kantin_menus WHERE id = %s FOR UPDATE",
            (body.menu_id,),
        )
        menu = cur.fetchone()
        if menu is None:
            raise HTTPException(status_code=400, detail="Menu tidak ditemukan")
        if menu["stock"] < body.qty:
            raise HTTPException(status_code=409, detail="Stok tidak cukup")

        subtotal = menu["price"] * body.qty
        total = subtotal
        if subtotal >= aturan.BATAS_DISKON:
            total = subtotal * (100 - aturan.DISKON_PERSEN) // 100

        cur.execute(
            "UPDATE kantin_menus SET stock = stock - %s WHERE id = %s",
            (body.qty, body.menu_id),
        )
        cur.execute(
            "INSERT INTO kantin_orders (menu_id, qty, total, status) VALUES (%s, %s, %s, %s)",
            (body.menu_id, body.qty, total, "baru"),
        )
        cur.execute(f"SELECT {KOLOM} FROM kantin_orders WHERE id = %s", (cur.lastrowid,))
        return cur.fetchone()


@router.get("/{order_id}", response_model=Order)
def detail_pesanan(order_id: int):
    pesanan = fetch_one(f"SELECT {KOLOM} FROM kantin_orders WHERE id = %s", (order_id,))
    if pesanan is None:
        raise HTTPException(status_code=404, detail=f"Pesanan {order_id} tidak ditemukan")
    return pesanan


@router.post("/{order_id}/batal", response_model=Order)
def batalkan_pesanan(order_id: int):
    with transaksi_pesanan() as cur:
        # Kunci pesanan agar pembatalan yang bersamaan hanya mengembalikan stok sekali.
        cur.execute(
            f"SELECT {KOLOM} FROM kantin_orders WHERE id = %s FOR UPDATE",
            (order_id,),
        )
        pesanan = cur.fetchone()
        if pesanan is None:
            raise HTTPException(status_code=404, detail=f"Pesanan {order_id} tidak ditemukan")
        if pesanan["status"] == "batal":
            raise HTTPException(status_code=409, detail="Pesanan sudah dibatalkan")

        cur.execute("UPDATE kantin_orders SET status = %s WHERE id = %s", ("batal", order_id))
        cur.execute(
            "UPDATE kantin_menus SET stock = stock + %s WHERE id = %s",
            (pesanan["qty"], pesanan["menu_id"]),
        )
        pesanan["status"] = "batal"
        return pesanan


@router.get("", response_model=list[Order])
def daftar_pesanan(status: StatusPesanan | None = None):
    sql = f"SELECT {KOLOM} FROM kantin_orders"
    if status is None:
        return fetch_all(f"{sql} ORDER BY id")
    return fetch_all(f"{sql} WHERE status = %s ORDER BY id", (status,))


@laporan_router.get("", response_model=Laporan)
def laporan():
    return fetch_one(
        """
        SELECT COUNT(*) AS jumlah_pesanan, COALESCE(SUM(total), 0) AS pendapatan
        FROM kantin_orders
        WHERE status = %s
        """,
        ("baru",),
    )