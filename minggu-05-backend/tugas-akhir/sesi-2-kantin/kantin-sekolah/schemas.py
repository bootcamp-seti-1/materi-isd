"""Bentuk data yang masuk dan keluar.

Model keluaran (Menu, Order, Laporan) sudah jadi.
Model masukan (MenuCreate, MenuUpdate, OrderCreate) baru berisi tipe dasar:
tugasmu menambahkan aturannya sesuai README. Ambil angka aturan dari aturan.py.
"""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel

import aturan  # noqa: F401  (dipakai saat kamu menambahkan aturan)

Kategori = Literal["makanan", "minuman"]
StatusPesanan = Literal["baru", "batal"]


# ---------- Model masukan: TODO tambahkan aturannya ----------


class MenuCreate(BaseModel):
    name: str
    category: Kategori
    price: int
    stock: int = 0


class MenuUpdate(BaseModel):
    name: str | None = None
    category: Kategori | None = None
    price: int | None = None
    stock: int | None = None


class OrderCreate(BaseModel):
    menu_id: int
    qty: int


# ---------- Model keluaran: sudah jadi ----------


class Menu(BaseModel):
    id: int
    name: str
    category: Kategori
    price: int
    stock: int
    created_at: datetime


class Order(BaseModel):
    id: int
    menu_id: int
    qty: int
    total: int
    status: StatusPesanan
    created_at: datetime


class Laporan(BaseModel):
    jumlah_pesanan: int
    pendapatan: int
