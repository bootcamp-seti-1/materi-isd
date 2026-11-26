"""Bentuk data yang masuk dan keluar.

Model keluaran (Menu, Order, Laporan) sudah jadi.
Model masukan (MenuCreate, MenuUpdate, OrderCreate) baru berisi tipe dasar:
tugasmu menambahkan aturannya sesuai README. Ambil angka aturan dari aturan.py.
"""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator

import aturan  # noqa: F401  (dipakai saat kamu menambahkan aturan)

Kategori = Literal["makanan", "minuman"]
StatusPesanan = Literal["baru", "batal"]


# ---------- Model masukan: TODO tambahkan aturannya ----------



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



class MenuCreate(BaseModel):
    name: str = Field(min_length=aturan.NAMA_MIN, max_length=aturan.NAMA_MAX)
    category: Kategori
    price: int = Field(ge=aturan.HARGA_MIN, le=aturan.HARGA_MAX)
    stock: int = Field(default=0, ge=0, le=aturan.STOK_MAX)

    model_config = {"extra": "forbid"}

    @field_validator("name")
    @classmethod
    def rapikan_nama(cls, v: str) -> str:
        v = v.strip()
        if len(v) < aturan.NAMA_MIN or len(v) > aturan.NAMA_MAX:
            raise ValueError(
                f"Nama harus {aturan.NAMA_MIN} sampai {aturan.NAMA_MAX} huruf"
            )
        return v

    @field_validator("price")
    @classmethod
    def cek_kelipatan(cls, v: int) -> int:
        if v % aturan.KELIPATAN_HARGA != 0:
            raise ValueError(
                f"Harga harus kelipatan {aturan.KELIPATAN_HARGA}"
            )
        return v


class MenuUpdate(BaseModel):
    name: str | None = None
    category: Kategori | None = None
    price: int | None = None
    stock: int | None = None

    model_config = {"extra": "forbid"}

    @field_validator("name")
    @classmethod
    def rapikan_nama(cls, v: str | None) -> str | None:
        if v is None:
            return v
        v = v.strip()
        if len(v) < aturan.NAMA_MIN or len(v) > aturan.NAMA_MAX:
            raise ValueError(
                f"Nama harus {aturan.NAMA_MIN} sampai {aturan.NAMA_MAX} huruf"
            )
        return v

    @field_validator("price")
    @classmethod
    def cek_kelipatan(cls, v: int | None) -> int | None:
        if v is None:
            return v
        if v < aturan.HARGA_MIN or v > aturan.HARGA_MAX:
            raise ValueError(
                f"Harga {aturan.HARGA_MIN} sampai {aturan.HARGA_MAX}"
            )
        if v % aturan.KELIPATAN_HARGA != 0:
            raise ValueError(
                f"Harga harus kelipatan {aturan.KELIPATAN_HARGA}"
            )
        return v

    @field_validator("stock")
    @classmethod
    def cek_stok(cls, v: int | None) -> int | None:
        if v is None:
            return v
        if v < 0 or v > aturan.STOK_MAX:
            raise ValueError(f"Stok 0 sampai {aturan.STOK_MAX}")
        return v


class OrderCreate(BaseModel):
    menu_id: int = Field(gt=0)
    qty: int = Field(ge=aturan.QTY_MIN, le=aturan.QTY_MAX)

    model_config = {"extra": "forbid"}


