# from db import fetch_all, execute
# import aturan


# class Koperasi:
#     def isi(self, nama, nominal):
#         """Tambah saldo siswa. Cek berurutan:
#         1. nama siswa tidak ada -> cetak "Siswa tidak ditemukan"
#         2. nominal bukan bilangan bulat 1 atau lebih -> cetak "Nominal tidak valid"
#         Kalau lolos, saldo siswa bertambah sebesar nominal. Tidak mencetak apa pun."""
#         # TODO
#         pass

#     def saldo(self, nama):
#         """Cetak satu baris:  Andi saldo : 30000
#         Kalau nama siswa tidak ada, cetak "Siswa tidak ditemukan"."""
#         # TODO
#         pass

#     def beli(self, nama, barang, jumlah):
#         """Siswa membeli barang. Cek berurutan, berhenti di kegagalan pertama dan
#         tidak ada data yang berubah:
#         1. siswa tidak ada                         -> "Siswa tidak ditemukan"
#         2. barang tidak ada                        -> "Barang tidak ditemukan"
#         3. jumlah bukan bilangan bulat 1 atau lebih -> "Jumlah tidak valid"
#         4. jumlah barang itu yang sudah dibeli siswa ini (yang tidak dibatalkan)
#            ditambah jumlah baru melebihi aturan.BATAS_PER_BARANG
#                                                    -> "Melebihi batas pembelian"
#         5. stok barang kurang dari jumlah          -> "Stok tidak cukup"
#         6. saldo siswa kurang dari total bayar     -> "Saldo tidak cukup"
#         Total bayar = harga x jumlah. Kalau harga x jumlah mencapai aturan.DISKON_MULAI
#         atau lebih, total bayar dipotong aturan.DISKON_PERSEN persen.
#         Kalau lolos: saldo berkurang sebesar total bayar, stok berkurang sebesar jumlah,
#         dan satu baris pembelian dicatat. Tidak mencetak apa pun."""
#         # TODO
#         pass

#     def laporan(self):
#         """Cetak satu baris per barang, urut dari pendapatan terbesar. Kalau pendapatan
#         sama, urut nama barang dari A sampai Z. Barang yang belum terjual tetap dicetak:
#             Pensil 3 buah pendapatan : 6000
#         Pembelian yang dibatalkan tidak dihitung. Baris terakhir adalah jumlah semuanya:
#             TOTAL 3 buah pendapatan : 6000"""
#         # TODO
#         pass

#     def stok(self):
#         """BONUS. Cetak satu baris per barang, urut sesuai nomor barang (id):
#             Buku_Tulis stok : 20"""
#         # TODO
#         pass

#     def batal(self, nomor):
#         """BONUS. Batalkan pembelian berdasarkan nomor pembelian. Cek berurutan:
#         1. nomor bukan bilangan bulat 1 atau lebih, atau tidak ada -> "Pembelian tidak ditemukan"
#         2. pembelian itu sudah dibatalkan                            -> "Pembelian sudah dibatalkan"
#         Kalau lolos: pembelian ditandai batal, saldo siswa bertambah sebesar total yang
#         dulu dibayar, dan stok barang bertambah sebesar jumlah yang dulu dibeli.
#         Tidak mencetak apa pun."""
#         # TODO
#         pass

from db import fetch_all, execute
import aturan


def _parse_bulat_positif(nilai):
    """Mengembalikan int >= 1 jika valid, atau None jika tidak valid."""
    if isinstance(nilai, bool):
        return None
    if isinstance(nilai, int):
        return nilai if nilai >= 1 else None
    if isinstance(nilai, str) and nilai.isascii() and nilai.isdigit():
        angka = int(nilai)
        return angka if angka >= 1 else None
    return None


class Koperasi:
    def isi(self, nama, nominal):
        """Tambah saldo siswa. Cek berurutan:
        1. nama siswa tidak ada -> cetak "Siswa tidak ditemukan"
        2. nominal bukan bilangan bulat 1 atau lebih -> cetak "Nominal tidak valid"
        Kalau lolos, saldo siswa bertambah sebesar nominal. Tidak mencetak apa pun.
        """
        siswa = fetch_all("SELECT id FROM students WHERE BINARY name = %s", (nama,))
        if not siswa:
            print("Siswa tidak ditemukan")
            return

        angka_nominal = _parse_bulat_positif(nominal)
        if angka_nominal is None:
            print("Nominal tidak valid")
            return

        execute(
            "UPDATE students SET balance = balance + %s WHERE id = %s",
            (angka_nominal, siswa[0]["id"]),
        )

    def saldo(self, nama):
        """Cetak satu baris:  Andi saldo : 30000
        Kalau nama siswa tidak ada, cetak "Siswa tidak ditemukan".
        """
        siswa = fetch_all(
            "SELECT name, balance FROM students WHERE BINARY name = %s", (nama,)
        )
        if not siswa:
            print("Siswa tidak ditemukan")
            return

        print(f"{siswa[0]['name']} saldo : {int(siswa[0]['balance'])}")

    def beli(self, nama, barang, jumlah):
        """Siswa membeli barang. Cek berurutan, berhenti di kegagalan pertama dan
        tidak ada data yang berubah:
        1. siswa tidak ada                         -> "Siswa tidak ditemukan"
        2. barang tidak ada                        -> "Barang tidak ditemukan"
        3. jumlah bukan bilangan bulat 1 atau lebih -> "Jumlah tidak valid"
        4. jumlah barang itu yang sudah dibeli siswa ini (yang tidak dibatalkan)
           ditambah jumlah baru melebihi aturan.BATAS_PER_BARANG
                                                   -> "Melebihi batas pembelian"
        5. stok barang kurang dari jumlah          -> "Stok tidak cukup"
        6. saldo siswa kurang dari total bayar     -> "Saldo tidak cukup"
        Total bayar = harga x jumlah. Kalau harga x jumlah mencapai aturan.DISKON_MULAI
        atau lebih, total bayar dipotong aturan.DISKON_PERSEN persen.
        Kalau lolos: saldo berkurang sebesar total bayar, stok berkurang sebesar jumlah,
        dan satu baris pembelian dicatat. Tidak mencetak apa pun.
        """
        siswa_rows = fetch_all(
            "SELECT id, balance FROM students WHERE BINARY name = %s", (nama,)
        )
        if not siswa_rows:
            print("Siswa tidak ditemukan")
            return
        siswa = siswa_rows[0]

        barang_rows = fetch_all(
            "SELECT id, price, stock FROM items WHERE BINARY name = %s", (barang,)
        )
        if not barang_rows:
            print("Barang tidak ditemukan")
            return
        item = barang_rows[0]

        angka_jumlah = _parse_bulat_positif(jumlah)
        if angka_jumlah is None:
            print("Jumlah tidak valid")
            return

        riwayat = fetch_all(
            """
            SELECT COALESCE(SUM(qty), 0) AS total_beli
            FROM purchases
            WHERE student_id = %s AND item_id = %s AND status = 'ok'
            """,
            (siswa["id"], item["id"]),
        )
        sudah_dibeli = int(riwayat[0]["total_beli"])
        if sudah_dibeli + angka_jumlah > aturan.BATAS_PER_BARANG:
            print("Melebihi batas pembelian")
            return

        if int(item["stock"]) < angka_jumlah:
            print("Stok tidak cukup")
            return

        subtotal = int(item["price"]) * angka_jumlah
        if subtotal >= aturan.DISKON_MULAI:
            total_bayar = subtotal - (subtotal * aturan.DISKON_PERSEN // 100)
        else:
            total_bayar = subtotal

        if int(siswa["balance"]) < total_bayar:
            print("Saldo tidak cukup")
            return

        execute(
            "UPDATE students SET balance = balance - %s WHERE id = %s",
            (total_bayar, siswa["id"]),
        )
        execute(
            "UPDATE items SET stock = stock - %s WHERE id = %s",
            (angka_jumlah, item["id"]),
        )
        execute(
            """
            INSERT INTO purchases (student_id, item_id, qty, total, status)
            VALUES (%s, %s, %s, %s, 'ok')
            """,
            (siswa["id"], item["id"], angka_jumlah, total_bayar),
        )

    def laporan(self):
        """Cetak satu baris per barang, urut dari pendapatan terbesar. Kalau pendapatan
        sama, urut nama barang dari A sampai Z. Barang yang belum terjual tetap dicetak:
            Pensil 3 buah pendapatan : 6000
        Pembelian yang dibatalkan tidak dihitung. Baris terakhir adalah jumlah semuanya:
            TOTAL 3 buah pendapatan : 6000
        """
        rows = fetch_all(
            """
            SELECT
                i.name,
                COALESCE(SUM(CASE WHEN p.status = 'ok' THEN p.qty ELSE 0 END), 0) AS terjual,
                COALESCE(SUM(CASE WHEN p.status = 'ok' THEN p.total ELSE 0 END), 0) AS pendapatan
            FROM items i
            LEFT JOIN purchases p ON p.item_id = i.id
            GROUP BY i.id, i.name
            ORDER BY pendapatan DESC, BINARY i.name ASC
            """
        )
        total_buah = 0
        total_pendapatan = 0
        for r in rows:
            terjual = int(r["terjual"])
            pendapatan = int(r["pendapatan"])
            total_buah += terjual
            total_pendapatan += pendapatan
            print(f"{r['name']} {terjual} buah pendapatan : {pendapatan}")

        print(f"TOTAL {total_buah} buah pendapatan : {total_pendapatan}")

    def stok(self):
        """BONUS. Cetak satu baris per barang, urut sesuai nomor barang (id):
        Buku_Tulis stok : 20
        """
        rows = fetch_all("SELECT name, stock FROM items ORDER BY id ASC")
        for r in rows:
            print(f"{r['name']} stok : {int(r['stock'])}")

    def batal(self, nomor):
        """BONUS. Batalkan pembelian berdasarkan nomor pembelian. Cek berurutan:
        1. nomor bukan bilangan bulat 1 atau lebih, atau tidak ada -> "Pembelian tidak ditemukan"
        2. pembelian itu sudah dibatalkan                            -> "Pembelian sudah dibatalkan"
        Kalau lolos: pembelian ditandai batal, saldo siswa bertambah sebesar total yang
        dulu dibayar, dan stok barang bertambah sebesar jumlah yang dulu dibeli.
        Tidak mencetak apa pun.
        """
        angka_nomor = _parse_bulat_positif(nomor)
        if angka_nomor is None:
            print("Pembelian tidak ditemukan")
            return

        rows = fetch_all(
            """
            SELECT id, student_id, item_id, qty, total, status
            FROM purchases
            WHERE id = %s
            """,
            (angka_nomor,),
        )
        if not rows:
            print("Pembelian tidak ditemukan")
            return

        trx = rows[0]
        if trx["status"] == "batal":
            print("Pembelian sudah dibatalkan")
            return

        execute("UPDATE purchases SET status = 'batal' WHERE id = %s", (trx["id"],))
        execute(
            "UPDATE students SET balance = balance + %s WHERE id = %s",
            (int(trx["total"]), trx["student_id"]),
        )
        execute(
            "UPDATE items SET stock = stock + %s WHERE id = %s",
            (int(trx["qty"]), trx["item_id"]),
        )