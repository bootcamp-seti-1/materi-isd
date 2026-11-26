"""Bentuk data yang masuk dan keluar dari API kantin."""

from datetime import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

import aturan

Kategori = Literal["makanan", "minuman"]
StatusPesanan = Literal["baru", "batal"]


# Aturan ini dipakai bersama saat membuat dan mengubah menu.
NamaMenu = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=aturan.NAMA_MIN,
        max_length=aturan.NAMA_MAX,
    ),
]
HargaMenu = Annotated[
    int,
    Field(
        ge=aturan.HARGA_MIN,
        le=aturan.HARGA_MAX,
        multiple_of=aturan.KELIPATAN_HARGA,
    ),
]
StokMenu = Annotated[int, Field(ge=0, le=aturan.STOK_MAX)]


# ---------- Model masukan ----------


class MenuCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: NamaMenu
    category: Kategori
    price: HargaMenu
    stock: StokMenu = 0


class MenuUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    # Endpoint memeriksa null setelah memastikan menu ada.
    name: NamaMenu | None = None
    category: Kategori | None = None
    price: HargaMenu | None = None
    stock: StokMenu | None = None


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
