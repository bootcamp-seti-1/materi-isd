"""Bentuk data yang masuk dan keluar.

Model keluaran (Menu, Order, Laporan) sudah jadi.
Model masukan (MenuCreate, MenuUpdate, OrderCreate) baru berisi tipe dasar:
tugasmu menambahkan aturannya sesuai README. Ambil angka aturan dari aturan.py.
"""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

import aturan  # noqa: F401  (dipakai saat kamu menambahkan aturan)

Kategori = Literal["makanan", "minuman"]
StatusPesanan = Literal["baru", "batal"]


# ---------- Model masukan: TODO tambahkan aturannya ----------


class MenuCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=aturan.NAMA_MIN, max_length=aturan.NAMA_MAX, strip_whitespace=True)
    category: Kategori
    price: int = Field(ge=aturan.HARGA_MIN, le=aturan.HARGA_MAX, multiple_of=aturan.KELIPATAN_HARGA)
    stock: int = Field(default=0, ge=0, le=aturan.STOK_MAX)


class MenuUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str | None = Field(default=None, min_length=aturan.NAMA_MIN, max_length=aturan.NAMA_MAX, strip_whitespace=True)
    category: Kategori | None = None
    price: int | None = Field(default=None, ge=aturan.HARGA_MIN, le=aturan.HARGA_MAX, multiple_of=aturan.KELIPATAN_HARGA)
    stock: int | None = Field(default=None, ge=0, le=aturan.STOK_MAX)


class OrderCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    menu_id: int = Field(gt=0)
    qty: int = Field(ge=aturan.QTY_MIN, le=aturan.QTY_MAX)


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
