from contextlib import contextmanager

from fastapi import APIRouter, HTTPException, Query

from db import fetch_all, fetch_one, get_connection
from schemas import Kategori, Menu, MenuCreate, MenuUpdate

router = APIRouter(prefix="/v1/menus", tags=["menus"])

KOLOM = "id, name, category, price, stock, created_at"


def cari_menu(menu_id: int, cur=None) -> dict:
    sql = f"SELECT {KOLOM} FROM kantin_menus WHERE id = %s"
    if cur is None:
        menu = fetch_one(sql, (menu_id,))
    else:
        cur.execute(sql, (menu_id,))
        menu = cur.fetchone()

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


@contextmanager
def transaksi_menu():
    with get_connection() as conn, conn.cursor(dictionary=True) as cur:
        # Satu penulisan menu setiap kali agar cek nama dan simpan berjalan berurutan.
        # MySQL melepas kunci ini ketika koneksi ditutup.
        cur.execute("SELECT GET_LOCK(%s, %s) AS terkunci", ("kantin_api:nama_menu", 10))
        if cur.fetchone()["terkunci"] != 1:
            raise HTTPException(status_code=503, detail="Menu sedang diproses. Coba lagi.")

        conn.start_transaction()
        try:
            yield cur
            conn.commit()
        except Exception:
            conn.rollback()
            raise


@router.post("", response_model=Menu, status_code=201)
def buat_menu(body: MenuCreate):
    with transaksi_menu() as cur:
        cur.execute(
            "SELECT id FROM kantin_menus WHERE LOWER(name) = LOWER(%s) LIMIT 1",
            (body.name,),
        )
        if cur.fetchone() is not None:
            raise HTTPException(status_code=409, detail="Nama menu sudah ada")

        cur.execute(
            "INSERT INTO kantin_menus (name, category, price, stock) VALUES (%s, %s, %s, %s)",
            (body.name, body.category, body.price, body.stock),
        )
        return cari_menu(cur.lastrowid, cur)


@router.patch("/{menu_id}", response_model=Menu)
def ubah_menu(menu_id: int, body: MenuUpdate):
    with transaksi_menu() as cur:
        menu = cari_menu(menu_id, cur)
        perubahan = body.model_dump(exclude_unset=True)

        if None in perubahan.values():
            raise HTTPException(status_code=422, detail="Field yang dikirim tidak boleh null")
        if not perubahan:
            return menu

        if "name" in perubahan:
            cur.execute(
                "SELECT id FROM kantin_menus WHERE LOWER(name) = LOWER(%s) AND id <> %s LIMIT 1",
                (perubahan["name"], menu_id),
            )
            if cur.fetchone() is not None:
                raise HTTPException(status_code=409, detail="Nama menu sudah ada")

        # Nama kolom berasal dari field yang diizinkan oleh MenuUpdate.
        kolom_set = ", ".join(f"{kolom} = %s" for kolom in perubahan)
        cur.execute(
            f"UPDATE kantin_menus SET {kolom_set} WHERE id = %s",
            (*perubahan.values(), menu_id),
        )
        return cari_menu(menu_id, cur)
