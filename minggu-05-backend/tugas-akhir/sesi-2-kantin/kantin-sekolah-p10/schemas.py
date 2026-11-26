"""Bentuk data yang masuk dan keluar.

Model keluaran (Menu, Order, Laporan) sudah jadi.
Model masukan (MenuCreate, MenuUpdate, OrderCreate) baru berisi tipe dasar:
tugasmu menambahkan aturannya sesuai README. Ambil angka aturan dari aturan.py.
"""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict

import aturan  # noqa: F401  (dipakai saat kamu menambahkan aturan)

Kategori = Literal["makanan", "minuman"]
StatusPesanan = Literal["baru", "batal"]


# ---------- Model masukan: TODO tambahkan aturannya ----------
#* SELF NOTE :

#* EXTRA UNKNOWN FIELD
#* - Extra unknown fields still not validated. Usually use ConfigDict(extra="forbid").
#* Because minimal import, Handle on router instead.
#? SOLVED : importing ConfigDict by Pydantic

#* EXPLICIT NULL 
#* - Explicit null when something like PATCH. Still need to catch explicit null values in PATCH /v1/menus/{menu_id}.
#* e.g via body.model_dump(exclude_unset=True) and return 422.
#* TL;DR -> NULL = NONE
#? SOLVED : Applied on router to deny null value (still allow none)

#* NON-STR TYPE ERROR RISK
#* _sanitize_text raises TypeError if called directly with a non-str;
#* inside Pydantic model_post_init, Pydantic handles type validation/coercion first, though raising ValueError is standard for validation errors. 
#? JUST DON'T CALL THE HELPER FUNCTION OUTSIDE PYDANTIC
#? Strict str value. Will raise TypeError that marked server-side 500 instead of 422 Unprocessable Content (user fault)

# ----------------- Validator functions ------------------- #
def _sanitize_text(value: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"Expected str, got {type(value).__name__}")
    return value.strip()

def _validate_name(value: str) -> str:
    result = _sanitize_text(value)
    if not (aturan.NAMA_MIN <= len(result) <= aturan.NAMA_MAX):
        raise ValueError(f"Panjang nama harus {aturan.NAMA_MIN} sampai {aturan.NAMA_MAX} karakter")
    return result
    
def _validate_price(value: int) -> int:
    if not (aturan.HARGA_MIN <= value <= aturan.HARGA_MAX):
        raise ValueError(f"Harga harus {aturan.HARGA_MIN} sampai {aturan.HARGA_MAX}")
    if value % aturan.KELIPATAN_HARGA != 0:
        raise ValueError(f"Harga harus kelipatan {aturan.KELIPATAN_HARGA}")
    return value

def _validate_stock(value: int) -> int:
    if not (0 <= value <= aturan.STOK_MAX):
        raise ValueError(f"Stok harus 0 sampai {aturan.STOK_MAX}")
    return value

def _validate_positive_int(value: int, label: str) -> int:
    if value <= 0:
        raise ValueError(f"{label} harus lebih dari 0")
    return value

def _validate_qty(value: int) -> int:
    if not (aturan.QTY_MIN <= value <= aturan.QTY_MAX):
        raise ValueError(
            f"Jumlah harus {aturan.QTY_MIN} sampai {aturan.QTY_MAX}"
        )
    return value

# ----------------- Model ------------------- #
class MenuCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    category: Kategori
    price: int
    stock: int = 0

    def model_post_init(self, __context) -> None:
        self.name = _validate_name(self.name)
        self.price = _validate_price(self.price)
        self.stock = _validate_stock(self.stock)

class MenuUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str | None = None
    category: Kategori | None = None
    price: int | None = None
    stock: int | None = None

    def model_post_init(self, __context) -> None:
        if self.name is not None:
            self.name = _validate_name(self.name)
        if self.price is not None:
            self.price = _validate_price(self.price)
        if self.stock is not None:
            self.stock = _validate_stock(self.stock)

class OrderCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    menu_id: int
    qty: int

    def model_post_init(self, __context) -> None:
        self.menu_id = _validate_positive_int(self.menu_id, "menu_id")
        self.qty = _validate_qty(self.qty)


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
