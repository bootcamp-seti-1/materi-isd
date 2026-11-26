from fastapi import APIRouter, HTTPException, Query

from db import execute, fetch_all, fetch_one, insert  # noqa: F401
from schemas import Kategori, Menu, MenuCreate, MenuUpdate

router = APIRouter(prefix="/v1/menus", tags=["menus"])

KOLOM = "id, name, category, price, stock, created_at"


def cari_menu(menu_id: int) -> dict:
    menu = fetch_one(f"SELECT {KOLOM} FROM kantin_menus WHERE id = %s", (menu_id,))
    if menu is None:
        raise HTTPException(status_code=404, detail=f"Menu {menu_id} tidak ditemukan")
    return menu


# ---------- Sudah jadi: contoh untukmu ----------


@router.get("", response_model=list[Menu])
def daftar_menu(
    category: Kategori | None = None,
    limit: int = Query(default=10, ge=1, le=50),
    offset: int = Query(default=0, ge=0),
):
    syarat = []
    params = []
    if category is not None:
        syarat.append("category = %s")
        params.append(category)
    where = f"WHERE {' AND '.join(syarat)}" if syarat else ""
    sql = f"SELECT {KOLOM} FROM kantin_menus {where} ORDER BY id LIMIT %s OFFSET %s"
    params += [limit, offset]
    return fetch_all(sql, tuple(params))


@router.get("/{menu_id}", response_model=Menu)
def detail_menu(menu_id: int):
    return cari_menu(menu_id)


# ---------- TODO: kerjakan sesuai README ----------


@router.post("", response_model=Menu, status_code=201)
def buat_menu(body: MenuCreate):
    # 1. Cek nama duplikat (case-insensitive)
    bentrok = fetch_one(
        "SELECT id FROM kantin_menus WHERE LOWER(name) = LOWER(%s)",
        (body.name,),
    )
    if bentrok is not None:
        raise HTTPException(status_code=409, detail="Nama menu sudah ada")

    # 2. Simpan
    new_id = insert(
        "INSERT INTO kantin_menus (name, category, price, stock) VALUES (%s, %s, %s, %s)",
        (body.name, body.category, body.price, body.stock),
    )

    # 3. Kembalikan menu yang baru dibuat (lengkap dengan created_at)
    return cari_menu(new_id)


# ---------- UBAH MENU ----------


@router.patch("/{menu_id}", response_model=Menu)
def ubah_menu(menu_id: int, body: MenuUpdate):
    # 1. Cek menu ada
    menu_lama = cari_menu(menu_id)  # otomatis 404 kalau tidak ada

    # 2. Ambil field yang benar-benar dikirim (bukan default None)
    dikirim = body.model_dump(exclude_unset=True)

    # 3. Tolak kalau ada field yang dikirim eksplisit bernilai null
    for nilai in dikirim.values():
        if nilai is None:
            raise HTTPException(
                status_code=422,
                detail="Field tidak boleh bernilai null",
            )

    # 4. Kalau name diubah, cek bentrok dengan menu LAIN
    if "name" in dikirim:
        bentrok = fetch_one(
            "SELECT id FROM kantin_menus WHERE LOWER(name) = LOWER(%s) AND id <> %s",
            (dikirim["name"], menu_id),
        )
        if bentrok is not None:
            raise HTTPException(status_code=409, detail="Nama menu sudah ada")

    # 5. Update hanya field yang dikirim
    if dikirim:
        set_parts = []
        params = []
        for kolom, nilai in dikirim.items():
            set_parts.append(f"{kolom} = %s")
            params.append(nilai)
        params.append(menu_id)
        sql = f"UPDATE kantin_menus SET {', '.join(set_parts)} WHERE id = %s"
        execute(sql, tuple(params))

    # 6. Kembalikan data terbaru
    return cari_menu(menu_id)