import os

import mysql.connector

# Diambil dari file .env lewat `uv run --env-file .env ...`.
# Password tidak lagi ditulis di kode, jadi aman di-push ke GitHub.
DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "127.0.0.1"),
    "user": os.environ["DB_USER"],
    "password": os.environ["DB_PASSWORD"],
    "database": os.environ.get("DB_NAME", "sakura_db"),
}


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def fetch_all(sql, params=()):
    conn = get_connection()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, params)
        return cur.fetchall()
    finally:
        conn.close()


def fetch_one(sql, params=()):
    rows = fetch_all(sql, params)
    return rows[0] if rows else None


def execute(sql, params=()):
    """UPDATE / DELETE. Mengembalikan jumlah baris yang terkena."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        return cur.rowcount
    finally:
        conn.close()


def insert(sql, params=()):
    """INSERT. Mengembalikan id baris yang baru dibuat (AUTO_INCREMENT)."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()
