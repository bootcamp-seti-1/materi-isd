"""Bentuk data yang masuk dan keluar.

Model keluaran (Menu, Order, Laporan) sudah jadi.
Model masukan (MenuCreate, MenuUpdate, OrderCreate) baru berisi tipe dasar:
tugasmu menambahkan aturannya sesuai README. Ambil angka aturan dari aturan.py.
"""

"""Bentuk data yang masuk dan keluar."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

import aturan

Kategori = Literal["makanan", "minuman"]
StatusPesanan = Literal["baru", "batal"]


class Masukan(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )


def cek_kelipatan_harga(nilai: int | None) -> int | None:
    if nilai is not None and nilai % aturan.KELIPATAN_HARGA != 0:
        raise ValueError(f"price harus kelipatan {aturan.KELIPATAN_HARGA}")
    return nilai


# ---------- Model masukan ----------


class MenuCreate(Masukan):
    name: str = Field(min_length=aturan.NAMA_MIN, max_length=aturan.NAMA_MAX)
    category: Kategori
    price: int = Field(ge=aturan.HARGA_MIN, le=aturan.HARGA_MAX)
    stock: int = Field(default=0, ge=0, le=aturan.STOK_MAX)

    @field_validator("price")
    @classmethod
    def validasi_price(cls, nilai: int) -> int:
        return cek_kelipatan_harga(nilai)


class MenuUpdate(Masukan):
    name: str | None = Field(default=None, min_length=aturan.NAMA_MIN, max_length=aturan.NAMA_MAX)
    category: Kategori | None = None
    price: int | None = Field(default=None, ge=aturan.HARGA_MIN, le=aturan.HARGA_MAX)
    stock: int | None = Field(default=None, ge=0, le=aturan.STOK_MAX)

    @field_validator("price")
    @classmethod
    def validasi_price(cls, nilai: int | None) -> int | None:
        return cek_kelipatan_harga(nilai)


class OrderCreate(Masukan):
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
