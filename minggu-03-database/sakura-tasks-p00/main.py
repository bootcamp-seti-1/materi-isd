import mysql.connector

from db import fetch_all, execute


def tampilkan_proyek():
    rows = fetch_all("SELECT id, name, client FROM projects ORDER BY id")
    print("\n=== Daftar Proyek ===")
    for r in rows:
        print(f"{r['id']}. {r['name']} (klien: {r['client']})")


def tampilkan_tugas():
    sql = """
        SELECT t.id, t.title, t.status, t.priority, p.name AS project_name
        FROM tasks t
        JOIN projects p ON p.id = t.project_id
        ORDER BY t.priority, t.id
    """
    rows = fetch_all(sql)
    print("\n=== Daftar Tugas ===")
    for r in rows:
        print(
            f"[{r['id']}] {r['title']} | {r['status']} | "
            f"P{r['priority']} | {r['project_name']}"
        )


def tambah_tugas():
    print("Fitur ini belum dibuat (menu 3)")


def ubah_status():
    print("Fitur ini belum dibuat (menu 4)")


def hapus_tugas():
    print("Fitur ini belum dibuat (menu 5)")


def laporan():
    print("Fitur ini belum dibuat (menu 6)")


MENU = """
=== Sakura Tasks ===
1. Lihat proyek
2. Lihat tugas
3. Tambah tugas
4. Ubah status tugas
5. Hapus tugas
6. Laporan jumlah tugas per proyek
0. Keluar
"""

AKSI = {
    "1": tampilkan_proyek,
    "2": tampilkan_tugas,
    "3": tambah_tugas,
    "4": ubah_status,
    "5": hapus_tugas,
    "6": laporan,
}


def main():
    while True:
        print(MENU)
        pilihan = input("Pilih menu: ").strip()
        if pilihan == "0":
            print("Sampai jumpa!")
            break
        aksi = AKSI.get(pilihan)
        if aksi is None:
            print("Menu tidak dikenal.")
            continue
        try:
            aksi()
        except mysql.connector.Error as e:
            print(f"Ada masalah di database: {e}")


if __name__ == "__main__":
    main()
