from db import fetch_all, execute
import aturan


def _parse_bilangan_bulat_positif(nilai):
    """Kembalikan (True, int_val) jika nilai adalah bilangan bulat >= 1,
    selain itu (False, None)."""
    if isinstance(nilai, bool):
        return False, None
    if isinstance(nilai, int):
        angka = nilai
    elif isinstance(nilai, str):
        teks = nilai.strip()
        if teks.startswith("+"):
            teks = teks[1:]
        if not teks.isdigit():
            return False, None
        angka = int(teks)
    else:
        return False, None

    if angka < 1:
        return False, None
    return True, angka


class Koperasi:
    def isi(self, nama, nominal):
        """Tambah saldo siswa. Cek berurutan:
        1. nama siswa tidak ada -> cetak "Siswa tidak ditemukan"
        2. nominal bukan bilangan bulat 1 atau lebih -> cetak "Nominal tidak valid"
        Kalau lolos, saldo siswa bertambah sebesar nominal. Tidak mencetak apa pun."""
        siswa = fetch_all(
            "SELECT id, balance FROM students WHERE name = %s",
            (nama,),
        )
        if not siswa:
            print("Siswa tidak ditemukan")
            return

        valid, nominal_int = _parse_bilangan_bulat_positif(nominal)
        if not valid:
            print("Nominal tidak valid")
            return

        execute(
            "UPDATE students SET balance = balance + %s WHERE id = %s",
            (nominal_int, siswa[0]["id"]),
        )

    def saldo(self, nama):
        """Cetak satu baris:  Andi saldo : 30000
        Kalau nama siswa tidak ada, cetak "Siswa tidak ditemukan"."""
        siswa = fetch_all(
            "SELECT name, balance FROM students WHERE name = %s",
            (nama,),
        )
        if not siswa:
            print("Siswa tidak ditemukan")
            return

        print(f"{siswa[0]['name']} saldo : {siswa[0]['balance']}")

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
        siswa = fetch_all(
            "SELECT id, balance FROM students WHERE name = %s",
            (nama,),
        )
        if not siswa:
            print("Siswa tidak ditemukan")
            return

        item = fetch_all(
            "SELECT id, price, stock FROM items WHERE name = %s",
            (barang,),
        )
        if not item:
            print("Barang tidak ditemukan")
            return

        valid, jumlah_int = _parse_bilangan_bulat_positif(jumlah)
        if not valid:
            print("Jumlah tidak valid")
            return

        student_id = siswa[0]["id"]
        item_id = item[0]["id"]
        saldo_sekarang = siswa[0]["balance"]
        harga = item[0]["price"]
        stok_sekarang = item[0]["stock"]

        sudah_dibeli = fetch_all(
            """
            SELECT COALESCE(SUM(qty), 0) AS total_qty
            FROM purchases
            WHERE student_id = %s AND item_id = %s AND status != 'batal'
            """,
            (student_id, item_id),
        )
        total_qty_siswa = sudah_dibeli[0]["total_qty"]

        if total_qty_siswa + jumlah_int > aturan.BATAS_PER_BARANG:
            print("Melebihi batas pembelian")
            return

        if stok_sekarang < jumlah_int:
            print("Stok tidak cukup")
            return

        subtotal = harga * jumlah_int
        if subtotal >= aturan.DISKON_MULAI:
            potongan = subtotal * aturan.DISKON_PERSEN // (aturan.DISKON_PERSEN * (100 // aturan.DISKON_PERSEN))
            total_bayar = subtotal - potongan
        else:
            total_bayar = subtotal

        if saldo_sekarang < total_bayar:
            print("Saldo tidak cukup")
            return

        execute(
            "UPDATE students SET balance = balance - %s WHERE id = %s",
            (total_bayar, student_id),
        )
        execute(
            "UPDATE items SET stock = stock - %s WHERE id = %s",
            (jumlah_int, item_id),
        )
        execute(
            """
            INSERT INTO purchases (student_id, item_id, qty, total, status)
            VALUES (%s, %s, %s, %s, 'ok')
            """,
            (student_id, item_id, jumlah_int, total_bayar),
        )

    def laporan(self):
        """Cetak satu baris per barang, urut dari pendapatan terbesar. Kalau pendapatan
        sama, urut nama barang dari A sampai Z. Barang yang belum terjual tetap dicetak:
            Pensil 3 buah pendapatan : 6000
        Pembelian yang dibatalkan tidak dihitung. Baris terakhir adalah jumlah semuanya:
            TOTAL 3 buah pendapatan : 6000"""
        rows = fetch_all(
            """
            SELECT
                i.name AS name,
                COALESCE(SUM(CASE WHEN p.status = 'ok' THEN p.qty ELSE 0 END), 0) AS terjual,
                COALESCE(SUM(CASE WHEN p.status = 'ok' THEN p.total ELSE 0 END), 0) AS pendapatan
            FROM items i
            LEFT JOIN purchases p ON i.id = p.item_id
            GROUP BY i.id, i.name
            ORDER BY pendapatan DESC, i.name ASC
            """
        )

        total_buah = 0
        total_pendapatan = 0

        for row in rows:
            terjual = row["terjual"]
            pendapatan = row["pendapatan"]
            total_buah += terjual
            total_pendapatan += pendapatan
            print(f"{row['name']} {terjual} buah pendapatan : {pendapatan}")

        print(f"TOTAL {total_buah} buah pendapatan : {total_pendapatan}")

    def stok(self):
        """BONUS. Cetak satu baris per barang, urut sesuai nomor barang (id):
            Buku_Tulis stok : 20"""
        rows = fetch_all("SELECT name, stock FROM items ORDER BY id ASC")
        for row in rows:
            print(f"{row['name']} stok : {row['stock']}")

    def batal(self, nomor):
        """BONUS. Batalkan pembelian berdasarkan nomor pembelian. Cek berurutan:
        1. nomor bukan bilangan bulat 1 atau lebih, atau tidak ada -> "Pembelian tidak ditemukan"
        2. pembelian itu sudah dibatalkan                            -> "Pembelian sudah dibatalkan"
        Kalau lolos: pembelian ditandai batal, saldo siswa bertambah sebesar total yang
        dulu dibayar, dan stok barang bertambah sebesar jumlah yang dulu dibeli.
        Tidak mencetak apa pun."""
        valid, nomor_int = _parse_bilangan_bulat_positif(nomor)
        if not valid:
            print("Pembelian tidak ditemukan")
            return

        pembelian = fetch_all(
            """
            SELECT id, student_id, item_id, qty, total, status
            FROM purchases
            WHERE id = %s
            """,
            (nomor_int,),
        )
        if not pembelian:
            print("Pembelian tidak ditemukan")
            return

        data = pembelian[0]
        if data["status"] == "batal":
            print("Pembelian sudah dibatalkan")
            return

        execute(
            "UPDATE purchases SET status = 'batal' WHERE id = %s",
            (nomor_int,),
        )
        execute(
            "UPDATE students SET balance = balance + %s WHERE id = %s",
            (data["total"], data["student_id"]),
        )
        execute(
            "UPDATE items SET stock = stock + %s WHERE id = %s",
            (data["qty"], data["item_id"]),
        )