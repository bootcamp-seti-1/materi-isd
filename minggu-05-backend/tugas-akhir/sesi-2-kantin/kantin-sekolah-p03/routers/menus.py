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
    nama_sama = fetch_one(
        "SELECT id FROM kantin_menus WHERE LOWER(name) = LOWER(%s)",
        (body.name,),
    )
    if nama_sama is not None:
        raise HTTPException(status_code=409, detail="Nama menu sudah ada")

    menu_id = insert(
        """
        INSERT INTO kantin_menus (name, category, price, stock)
        VALUES (%s, %s, %s, %s)
        """,
        (body.name, body.category, body.price, body.stock),
    )
    return cari_menu(menu_id)


@router.patch("/{menu_id}", response_model=Menu)
def ubah_menu(menu_id: int, body: MenuUpdate):
    menu = cari_menu(menu_id)
    perubahan = body.model_dump(exclude_unset=True)

    if any(nilai is None for nilai in perubahan.values()):
        raise HTTPException(status_code=422, detail="Field tidak boleh null")

    if "name" in perubahan:
        nama_sama = fetch_one(
            """
            SELECT id FROM kantin_menus
            WHERE LOWER(name) = LOWER(%s) AND id <> %s
            """,
            (perubahan["name"], menu_id),
        )
        if nama_sama is not None:
            raise HTTPException(status_code=409, detail="Nama menu sudah ada")

    if not perubahan:
        return menu

    kolom_diizinkan = {"name", "category", "price", "stock"}
    set_clause = ", ".join(
        f"{kolom} = %s" for kolom in perubahan if kolom in kolom_diizinkan
    )
    execute(
        f"UPDATE kantin_menus SET {set_clause} WHERE id = %s",
        (*perubahan.values(), menu_id),
    )
    return cari_menu(menu_id)
