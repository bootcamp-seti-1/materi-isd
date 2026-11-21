# import _mysql_connector
from db import fetch_all, execute
import aturan


class Koperasi:
    def isi(self, nama, nominal):
        """Tambah saldo siswa. Cek berurutan:
        1. nama siswa tidak ada -> cetak "Siswa tidak ditemukan"
        2. nominal bukan bilangan bulat 1 atau lebih -> cetak "Nominal tidak valid"
        Kalau lolos, saldo siswa bertambah sebesar nominal. Tidak mencetak apa pun."""
        # TODO
        if not fetch_all("SELECT * FROM students WHERE name = %s", (nama,)):
            print("Siswa tidak ditemukan")
            return

        if isinstance(nominal, bool) or not isinstance(nominal, (int, str)):
            print("Nominal tidak valid")
            return

        try:
            nominal = int(nominal)
        except (TypeError, ValueError):
            print("Nominal tidak valid")
            return

        if nominal < 1:
            print("Nominal tidak valid")
            return

        execute("UPDATE students SET balance = balance + %s WHERE name = %s", (nominal, nama))

    def saldo(self, nama):
        """Cetak satu baris:  Andi saldo : 30000
        Kalau nama siswa tidak ada, cetak "Siswa tidak ditemukan"."""
        # TODO
        if not fetch_all("SELECT * FROM students WHERE name = %s", (nama,)):
            print("Siswa tidak ditemukan")
            return
        result = fetch_all("SELECT balance FROM students WHERE name = %s", (nama,))
        print(f"{nama} saldo : {result[0]['balance']}")

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
        dan satu baris pembelian dicatat. Tidak mencetak apa pun."""
        # TODO
        #1
        if not fetch_all("SELECT * FROM students WHERE name = %s", (nama,)):
            print("Siswa tidak ditemukan")
            return
        #2
        elif not fetch_all("SELECT * FROM items WHERE name = %s", (barang,)):
            print("Barang tidak ditemukan")
            return
        #3
        try:
            jumlah = int(jumlah)
        except (TypeError, ValueError):
            print("Jumlah tidak valid")
            return
        if jumlah < 1:
            print("Jumlah tidak valid")
            return
        #4
        # if fetch_all("SELECT SUM(qty) AS total FROM purchases WHERE student_id = %s AND item_id = %s AND status = 'batal'", (nama, barang))[0]['total'] + jumlah > aturan.BATAS_PER_BARANG:
        #     print("Melebihi batas pembelian")
        #     return
        hasil = fetch_all(
            """
            SELECT COALESCE(SUM(p.qty), 0) AS total
            FROM purchases p
            JOIN students s ON s.id = p.student_id
            JOIN items i ON i.id = p.item_id
            WHERE s.name = %s
            AND i.name = %s
            AND p.status = 'ok'
            """,
            (nama, barang)
        )

        jumlah_dibeli = hasil[0]["total"]

        if jumlah_dibeli + jumlah > aturan.BATAS_PER_BARANG:
            print("Melebihi batas pembelian")
            return

        #5
        elif fetch_all("SELECT stock FROM items WHERE name = %s", (barang,))[0]['stock'] < jumlah:
            print("Stok tidak cukup")
            return
        #6
        harga = fetch_all("SELECT price FROM items WHERE name = %s", (barang,))[0]['price']
        total_bayar = harga * jumlah
        if total_bayar >= aturan.DISKON_MULAI:
            total_bayar -= total_bayar * aturan.DISKON_PERSEN / 100
            # total_bayar = total_bayar - (total_bayar * aturan.DISKON_PERSEN / 100) (cara lain)
        if fetch_all("SELECT balance FROM students WHERE name = %s", (nama,))[0]['balance'] < total_bayar:
            print("Saldo tidak cukup")
            return
        #7
        student_id = fetch_all("SELECT id FROM students WHERE name = %s", (nama,))[0]['id']
        item_id = fetch_all("SELECT id FROM items WHERE name = %s", (barang,))[0]['id']
        execute("INSERT INTO purchases (student_id, item_id, qty, total, status) VALUES (%s, %s, %s, %s, 'ok')", (student_id, item_id, jumlah, total_bayar))
        execute("UPDATE students SET balance = balance - %s WHERE name = %s", (total_bayar, nama))
        execute("UPDATE items SET stock = stock - %s WHERE name = %s", (jumlah, barang))

    def laporan(self):
        """Cetak satu baris per barang, urut dari pendapatan terbesar. Kalau pendapatan
        sama, urut nama barang dari A sampai Z. Barang yang belum terjual tetap dicetak:
            Pensil 3 buah pendapatan : 6000
        Pembelian yang dibatalkan tidak dihitung. Baris terakhir adalah jumlah semuanya:
            TOTAL 3 buah pendapatan : 6000"""
        laporan = fetch_all("""
            SELECT i.name,
                   COALESCE(SUM(CASE WHEN p.status = 'ok' THEN p.qty ELSE 0 END), 0) AS qty,
                   COALESCE(SUM(CASE WHEN p.status = 'ok' THEN p.total ELSE 0 END), 0) AS pendapatan
            FROM items i
            LEFT JOIN purchases p ON p.item_id = i.id
            GROUP BY i.id, i.name
            ORDER BY pendapatan DESC, i.name ASC
        """)

        total_qty = 0
        total_pendapatan = 0

        for baris in laporan:
            qty = int(baris["qty"])
            pendapatan = int(baris["pendapatan"])
            print(f"{baris['name']} {qty} buah pendapatan : {pendapatan}")
            total_qty += qty
            total_pendapatan += pendapatan

        print(f"TOTAL {total_qty} buah pendapatan : {total_pendapatan}")

    def stok(self):
        """BONUS. Cetak satu baris per barang, urut sesuai nomor barang (id):
            Buku_Tulis stok : 20"""
        # TODO
        laporan = fetch_all("""
            SELECT name, stock
            FROM items
            ORDER BY id
        """)
        for baris in laporan:
            print(f"{baris['name']} stok : {baris['stock']}")

    def batal(self, nomor):
        """BONUS. Batalkan pembelian berdasarkan nomor pembelian. Cek berurutan:
        1. nomor bukan bilangan bulat 1 atau lebih, atau tidak ada -> "Pembelian tidak ditemukan"
        2. pembelian itu sudah dibatalkan                            -> "Pembelian sudah dibatalkan"
        Kalau lolos: pembelian ditandai batal, saldo siswa bertambah sebesar total yang
        dulu dibayar, dan stok barang bertambah sebesar jumlah yang dulu dibeli.
        Tidak mencetak apa pun."""
        # TODO
        try:
            nomor = int(nomor)
        except (TypeError, ValueError):
            print("Pembelian tidak ditemukan")
            return

        if nomor < 1:
            print("Pembelian tidak ditemukan")
            return

        pembelian = fetch_all("""
            SELECT p.qty, p.total, p.status,
                   s.name AS student_name, i.name AS item_name
            FROM purchases p
            JOIN students s ON s.id = p.student_id
            JOIN items i ON i.id = p.item_id
            WHERE p.id = %s
        """, (nomor,))

        if not pembelian:
            print("Pembelian tidak ditemukan")
            return

        pembelian = pembelian[0]

        if pembelian["status"] == "batal":
            print("Pembelian sudah dibatalkan")
            return

        execute("UPDATE purchases SET status = 'batal' WHERE id = %s", (nomor,))
        execute(
            "UPDATE students SET balance = balance + %s WHERE name = %s",
            (pembelian["total"], pembelian["student_name"])
        )
        execute(
            "UPDATE items SET stock = stock + %s WHERE name = %s",
            (pembelian["qty"], pembelian["item_name"])
        )
        