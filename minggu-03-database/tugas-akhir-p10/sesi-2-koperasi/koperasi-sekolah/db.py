import mysql.connector
from typing import Any, cast

# Ganti p00 pada baris "user" dengan ID-mu (huruf kecil), contoh: sakura_p03
DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "sakura_p10",
    "password": "RedskyTwilight",
    "database": "sakura_db",
}


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def fetch_all(sql: str, params: tuple[Any, ...] | dict[str, Any] = ()) -> list[dict[str, Any]]:
    conn = get_connection()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, params)
        return cast(list[dict[str, Any]], cur.fetchall())
    finally:
        conn.close()


def execute(sql, params=()):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        return cur.rowcount
    finally:
        conn.close()
