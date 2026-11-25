"""Server latihan Toko Sakura untuk kuis CTFd minggu 5.

Jalankan dari folder ini:
    uv run fastapi dev main.py --port 8100

Data disimpan di memori. Setiap server restart (termasuk saat file ini
disimpan), data kembali ke keadaan awal.
"""

from typing import Literal

from fastapi import FastAPI, HTTPException, Query, Response
from pydantic import BaseModel, ConfigDict, Field

app = FastAPI(title="Toko Sakura API (server soal)", version="0.1.0")

Kategori = Literal["atk", "minuman", "makanan"]

ITEMS = [
    {"id": 1, "name": "Buku Tulis", "category": "atk", "price": 5000, "stock": 40, "rak": "A-01"},
    {"id": 2, "name": "Pulpen Hitam", "category": "atk", "price": 3000, "stock": 100, "rak": "A-02"},
    {"id": 3, "name": "Penghapus", "category": "atk", "price": 2000, "stock": 30, "rak": "C-12"},
    {"id": 4, "name": "Spidol Papan", "category": "atk", "price": 9000, "stock": 12, "rak": "A-07"},
    {"id": 5, "name": "Penggaris 30cm", "category": "atk", "price": 4000, "stock": 25, "rak": "B-03"},
    {"id": 6, "name": "Air Mineral", "category": "minuman", "price": 3500, "stock": 48, "rak": "D-01"},
    {"id": 7, "name": "Teh Botol", "category": "minuman", "price": 5000, "stock": 36, "rak": "D-02"},
    {"id": 8, "name": "Kertas HVS A4", "category": "atk", "price": 52000, "stock": 10, "rak": "B-09"},
    {"id": 9, "name": "Roti Coklat", "category": "makanan", "price": 6000, "stock": 15, "rak": "E-04"},
]

MEMBERS = [
    {"id": 1, "name": "Budi", "pin": "1739"},
    {"id": 2, "name": "Sari", "pin": "2604"},
    {"id": 3, "name": "Rina", "pin": "4821"},
    {"id": 4, "name": "Dodi", "pin": "9150"},
]


class ItemCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    name: str = Field(min_length=3, max_length=50)
    price: int = Field(ge=500, le=1_000_000)
    category: Kategori = "atk"
    stock: int = Field(default=0, ge=0)


class ItemUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    name: str | None = Field(default=None, min_length=3, max_length=50)
    price: int | None = Field(default=None, ge=500, le=1_000_000)
    category: Kategori | None = None
    stock: int | None = Field(default=None, ge=0)


class Item(BaseModel):
    id: int
    name: str
    category: Kategori
    price: int
    stock: int


class MemberPublic(BaseModel):
    id: int
    name: str


def cari_item(item_id: int) -> dict:
    for item in ITEMS:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail=f"Barang {item_id} tidak ditemukan")


@app.get("/")
def beranda():
    return {"pesan": "Server soal Toko Sakura jalan", "dokumentasi": "/docs"}


@app.get("/v1/items", response_model=list[Item])
def daftar_item(
    category: Kategori | None = None,
    limit: int = Query(default=10, ge=1, le=50),
    offset: int = Query(default=0, ge=0),
):
    hasil = ITEMS
    if category is not None:
        hasil = [i for i in hasil if i["category"] == category]
    return hasil[offset : offset + limit]


@app.get("/v1/items/{item_id}", response_model=Item)
def detail_item(item_id: int, response: Response):
    item = cari_item(item_id)
    response.headers["X-Lokasi-Rak"] = item["rak"]
    return item


@app.get("/v1/items/termurah", response_model=Item)
def item_termurah():
    return min(ITEMS, key=lambda i: i["price"])


@app.post("/v1/items", response_model=Item, status_code=201)
def buat_item(body: ItemCreate):
    item = {"id": max(i["id"] for i in ITEMS) + 1, **body.model_dump(), "rak": "Z-99"}
    ITEMS.append(item)
    return item


@app.put("/v1/items/{item_id}", response_model=Item)
def ganti_item(item_id: int, body: ItemCreate):
    item = cari_item(item_id)
    item.update(body.model_dump())
    return item


@app.patch("/v1/items/{item_id}", response_model=Item)
def ubah_item(item_id: int, body: ItemUpdate):
    item = cari_item(item_id)
    item.update(body.model_dump(exclude_unset=True))
    return item


# Versi lama, ditulis anak magang sebelum ada review kode.
@app.patch("/v1/lama/items/{item_id}")
def ubah_item_versi_lama(item_id: int, body: ItemUpdate):
    item = cari_item(item_id)
    item.update(body.model_dump())
    return item


@app.get("/v1/members", response_model=list[MemberPublic])
def daftar_member():
    return MEMBERS


@app.get("/v1/members/{member_id}")
def detail_member(member_id: int):
    for m in MEMBERS:
        if m["id"] == member_id:
            return m
    raise HTTPException(status_code=404, detail=f"Member {member_id} tidak ditemukan")
