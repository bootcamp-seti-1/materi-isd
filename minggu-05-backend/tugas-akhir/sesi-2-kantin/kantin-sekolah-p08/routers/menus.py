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

def pastikan_nama_menu_belum_ada(nama_menu: str, kecuali_menu_id: int | None = None) -> None:
    sql = "SELECT id FROM kantin_menus WHERE LOWER(name) = LOWER(%s)"
    params: tuple[str | int, ...] = (nama_menu,)
    if kecuali_menu_id is not None:
        sql += " AND id <> %s"
        params += (kecuali_menu_id,)
    if fetch_one(sql, params) is not None:
        raise HTTPException(status_code=409, detail="Nama menu sudah ada")


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
    pastikan_nama_menu_belum_ada(body.name)
    menu_id = insert(
        "INSERT INTO kantin_menus (name, category, price, stock) VALUES (%s, %s, %s, %s)",
        (body.name, body.category, body.price, body.stock),
    )
    return cari_menu(menu_id)


@router.patch("/{menu_id}", response_model=Menu)
def ubah_menu(menu_id: int, body: MenuUpdate):
    cari_menu(menu_id)
    changes = body.model_dump(exclude_unset=True)
    if any(value is None for value in changes.values()):
        raise HTTPException(status_code=422, detail="Field tidak boleh null")
    if "name" in changes:
        pastikan_nama_menu_belum_ada(changes["name"], menu_id)
    if changes:
        set_clause = ", ".join(f"{field} = %s" for field in changes)
        execute(
            f"UPDATE kantin_menus SET {set_clause} WHERE id = %s",
            tuple(changes.values()) + (menu_id,),
        )
    return cari_menu(menu_id)