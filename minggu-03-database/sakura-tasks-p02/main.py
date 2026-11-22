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
    tampilkan_proyek()
    project_id = input("Nomor proyek: ").strip()
    judul = input("Judul tugas: ").strip()
    prioritas = input("Prioritas 1-3 (kosongkan untuk 2): ").strip()
    if not project_id.isdigit():
        print("Nomor proyek harus angka.")
        return
    if judul == "":
        print("Judul tugas tidak boleh kosong.")
        return
    if prioritas == "":
        prioritas = "2"
    if prioritas not in ("1", "2", "3"):
        print("Prioritas harus 1, 2, atau 3.")
        return
    execute(
        "INSERT INTO tasks (project_id, title, priority) VALUES (%s, %s, %s)",
        (project_id, judul, prioritas),
    )
    print(f"Tugas '{judul}' berhasil disimpan.")


def ubah_status():
    tampilkan_tugas()
    nomor = input("Nomor tugas: ").strip()
    status = input("Status baru (todo/doing/done): ").strip()
    if not nomor.isdigit():
        print("Nomor tugas harus angka.")
        return
    if status not in ("todo", "doing", "done"):
        print("Status harus todo, doing, atau done.")
        return
    ada = fetch_all("SELECT id FROM tasks WHERE id = %s", (nomor,))
    if not ada:
        print("Tugas tidak ditemukan.")
        return
    execute("UPDATE tasks SET status = %s WHERE id = %s", (status, nomor))
    print("Status tugas berhasil diubah.")


def hapus_tugas():
    tampilkan_tugas()
    nomor = input("Nomor tugas yang dihapus: ").strip()
    if not nomor.isdigit():
        print("Nomor tugas harus angka.")
        return
    baris = fetch_all("SELECT title FROM tasks WHERE id = %s", (nomor,))
    if not baris:
        print("Tugas tidak ditemukan.")
        return
    jawab = input(f"Yakin hapus '{baris[0]['title']}'? (y/n): ").strip().lower()
    if jawab != "y":
        print("Dibatalkan.")
        return
    execute("DELETE FROM tasks WHERE id = %s", (nomor,))
    print("Tugas dihapus.")

def laporan():
    sql = """
        SELECT p.name,
               COUNT(t.id) AS jumlah,
               COALESCE(SUM(t.status = 'done'), 0) AS selesai
        FROM projects p
        LEFT JOIN tasks t ON t.project_id = p.id
        GROUP BY p.id, p.name
        ORDER BY p.id
    """
    rows = fetch_all(sql)
    print("\n=== Laporan per Proyek ===")
    for r in rows:
        print(f"{r['name']}: {r['jumlah']} tugas, {r['selesai']} selesai")


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