from fastapi import APIRouter, HTTPException, Query

from db import execute, fetch_all, fetch_one, insert
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


# ---------- Endpoint menu ----------


@router.post("", response_model=Menu, status_code=201)
def buat_menu(body: MenuCreate):
    nama = body.name.strip()
    duplikat = fetch_one(
        "SELECT id FROM kantin_menus "
        "WHERE LOWER(TRIM(name)) = LOWER(TRIM(%s))",
        (nama,),
    )
    if duplikat is not None:
        raise HTTPException(status_code=409, detail="Nama menu sudah ada")

    menu_id = insert(
        "INSERT INTO kantin_menus (name, category, price, stock) "
        "VALUES (%s, %s, %s, %s)",
        (nama, body.category, body.price, body.stock),
    )
    return cari_menu(menu_id)


@router.patch("/{menu_id}", response_model=Menu)
def ubah_menu(menu_id: int, body: MenuUpdate):
    menu = cari_menu(menu_id)
    perubahan = body.model_dump(exclude_unset=True)

    if any(nilai is None for nilai in perubahan.values()):
        raise HTTPException(status_code=422, detail="Field tidak boleh null")

    if "name" in perubahan:
        nama = perubahan["name"].strip()
        duplikat = fetch_one(
            "SELECT id FROM kantin_menus "
            "WHERE LOWER(TRIM(name)) = LOWER(TRIM(%s)) AND id <> %s",
            (nama, menu_id),
        )
        if duplikat is not None:
            raise HTTPException(status_code=409, detail="Nama menu sudah ada")
        perubahan["name"] = nama

    kolom_diizinkan = ("name", "category", "price", "stock")
    kolom_diubah = [kolom for kolom in kolom_diizinkan if kolom in perubahan]
    if not kolom_diubah:
        return menu

    set_clause = ", ".join(f"{kolom} = %s" for kolom in kolom_diubah)
    params = tuple(perubahan[kolom] for kolom in kolom_diubah) + (menu_id,)
    execute(
        f"UPDATE kantin_menus SET {set_clause} WHERE id = %s",
        params,
    )
    return cari_menu(menu_id)
