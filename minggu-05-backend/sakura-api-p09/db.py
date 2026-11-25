import os

import mysql.connector

# Kamus (dictionary) konfigurasi koneksi ke database MySQL.
# Nilai diambil dari environment variable agar kredensial sensitif tidak ditulis langsung di kode.
DB_CONFIG = {
    # Mengambil DB_HOST dari environment; jika tidak diatur, gunakan default "127.0.0.1"
    "host": os.environ.get("DB_HOST", "127.0.0.1"),
    # Mengambil DB_USER dari environment (wajib ada; akan memunculkan KeyError jika belum diatur)
    "user": os.environ["DB_USER"],
    # Mengambil DB_PASSWORD dari environment (wajib ada; akan memunculkan KeyError jika belum diatur)
    "password": os.environ["DB_PASSWORD"],
    # Mengambil DB_NAME dari environment; jika tidak diatur, gunakan default "sakura_db"
    "database": os.environ.get("DB_NAME", "sakura_db"),
}


# Membuka dan mengembalikan koneksi baru ke server MySQL menggunakan isi DB_CONFIG
def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


# Menjalankan query SELECT untuk mengambil semua baris hasil sebagai list of dictionary
def fetch_all(sql, params=()):
    conn = get_connection()
    try:
        # dictionary=True mengubah tiap baris hasil menjadi dict (contoh: {"id": 1, "title": "..."})
        cur = conn.cursor(dictionary=True)
        # Menjalankan perintah SQL secara aman dengan memisahkan query dan parameter (%s)
        cur.execute(sql, params)
        # Mengambil dan mengembalikan seluruh baris hasil query
        return cur.fetchall()
    finally:
        # Memastikan koneksi database selalu ditutup kembali meskipun terjadi error
        conn.close()


# Menjalankan query SELECT dan hanya mengambil satu baris pertama (atau None jika data tidak ditemukan)
def fetch_one(sql, params=()):
    rows = fetch_all(sql, params)
    return rows[0] if rows else None


# Menjalankan query perubahan data (UPDATE atau DELETE) dan mengembalikan jumlah baris yang terpengaruh
def execute(sql, params=()):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        # Menyimpan perubahan data secara permanen ke database sebelum koneksi ditutup
        conn.commit()
        # Mengembalikan jumlah baris yang berubah/terhapus (0 jika tidak ada ID yang cocok)
        return cur.rowcount
    finally:
        # Menutup koneksi database
        conn.close()


# Menjalankan query INSERT untuk menambah data baru dan mengembalikan ID (AUTO_INCREMENT) yang baru dibuat
def insert(sql, params=()):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        # Menyimpan baris baru secara permanen ke database
        conn.commit()
        # Mengembalikan nilai primary key (id) dari baris yang baru saja dimasukkan
        return cur.lastrowid
    finally:
        # Menutup koneksi database
        conn.close() 