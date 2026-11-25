# Kode pencarian buatan vendor lama. TIDAK perlu dijalankan, cukup dibaca.

from db import fetch_all


def cari_produk(nama):
    """Mencari produk milik Toko A berdasarkan nama yang diketik pengguna."""
    sql = f"SELECT id, toko, nama, harga FROM soal8_produk WHERE toko = 'A' AND nama = '{nama}'"
    return fetch_all(sql)
