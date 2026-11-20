from db import fetch_all, execute
import aturan


class Koperasi:
    def _siswa(self, nama):
        for siswa in fetch_all("SELECT id, name, balance FROM students"):
            if siswa["name"] == nama:
                return siswa
        return None

    def _barang(self, nama):
        for barang in fetch_all("SELECT id, name, price, stock FROM items"):
            if barang["name"] == nama:
                return barang
        return None

    def _bilangan_positif(self, teks):
        if isinstance(teks, bool):
            return None
        if isinstance(teks, int):
            return teks if teks >= 1 else None
        if not isinstance(teks, str) or not teks.isascii() or not teks.isdigit():
            return None
        try:
            nilai = int(teks)
        except (TypeError, ValueError):
            return None
        return nilai if nilai >= 1 else None

    def isi(self, nama, nominal):
        """Tambah saldo siswa. Cek berurutan:
        1. nama siswa tidak ada -> cetak "Siswa tidak ditemukan"
        2. nominal bukan bilangan bulat 1 atau lebih -> cetak "Nominal tidak valid"
        Kalau lolos, saldo siswa bertambah sebesar nominal. Tidak mencetak apa pun."""
        siswa = self._siswa(nama)
        if siswa is None:
            print("Siswa tidak ditemukan")
            return

        nominal = self._bilangan_positif(nominal)
        if nominal is None:
            print("Nominal tidak valid")
            return

        execute(
            "UPDATE students SET balance = balance + %s WHERE id = %s",
            (nominal, siswa["id"]),
        )

    def saldo(self, nama):
        """Cetak satu baris:  Andi saldo : 30000
        Kalau nama siswa tidak ada, cetak "Siswa tidak ditemukan"."""
        siswa = self._siswa(nama)
        if siswa is None:
            print("Siswa tidak ditemukan")
            return
        print(f'{siswa["name"]} saldo : {int(siswa["balance"])}')

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
        siswa = self._siswa(nama)
        if siswa is None:
            print("Siswa tidak ditemukan")
            return

        barang_data = self._barang(barang)
        if barang_data is None:
            print("Barang tidak ditemukan")
            return

        jumlah = self._bilangan_positif(jumlah)
        if jumlah is None:
            print("Jumlah tidak valid")
            return

        sudah_dibeli = fetch_all(
            """
            SELECT COALESCE(SUM(qty), 0) AS jumlah
            FROM purchases
            WHERE student_id = %s AND item_id = %s AND status = 'ok'
            """,
            (siswa["id"], barang_data["id"]),
        )[0]["jumlah"]
        sudah_dibeli = int(sudah_dibeli)
        if sudah_dibeli + jumlah > aturan.BATAS_PER_BARANG:
            print("Melebihi batas pembelian")
            return

        if int(barang_data["stock"]) < jumlah:
            print("Stok tidak cukup")
            return

        subtotal = int(barang_data["price"]) * jumlah
        total = subtotal
        if subtotal >= aturan.DISKON_MULAI:
            potongan = subtotal * aturan.DISKON_PERSEN // 100
            total = subtotal - potongan

        if int(siswa["balance"]) < total:
            print("Saldo tidak cukup")
            return

        execute(
            "UPDATE students SET balance = balance - %s WHERE id = %s",
            (total, siswa["id"]),
        )
        execute(
            "UPDATE items SET stock = stock - %s WHERE id = %s",
            (jumlah, barang_data["id"]),
        )
        execute(
            """
            INSERT INTO purchases (student_id, item_id, qty, total, status)
            VALUES (%s, %s, %s, %s, 'ok')
            """,
            (siswa["id"], barang_data["id"], jumlah, total),
        )

    def laporan(self):
        """Cetak satu baris per barang, urut dari pendapatan terbesar. Kalau pendapatan
        sama, urut nama barang dari A sampai Z. Barang yang belum terjual tetap dicetak:
            Pensil 3 buah pendapatan : 6000
        Pembelian yang dibatalkan tidak dihitung. Baris terakhir adalah jumlah semuanya:
            TOTAL 3 buah pendapatan : 6000"""
        barang = fetch_all(
            """
            SELECT i.id, i.name,
                   COALESCE(SUM(CASE WHEN p.status = 'ok' THEN p.qty ELSE 0 END), 0) AS qty,
                   COALESCE(SUM(CASE WHEN p.status = 'ok' THEN p.total ELSE 0 END), 0) AS pendapatan
            FROM items i
            LEFT JOIN purchases p ON p.item_id = i.id
            GROUP BY i.id, i.name
            """
        )

        data = [
            (row["name"], int(row["qty"]), int(row["pendapatan"]))
            for row in barang
        ]
        data.sort(key=lambda row: (-row[2], row[0]))

        total_qty = 0
        total_pendapatan = 0
        for nama, qty, pendapatan in data:
            print(f"{nama} {qty} buah pendapatan : {pendapatan}")
            total_qty += qty
            total_pendapatan += pendapatan
        print(f"TOTAL {total_qty} buah pendapatan : {total_pendapatan}")

    def stok(self):
        """BONUS. Cetak satu baris per barang, urut sesuai nomor barang (id):
            Buku_Tulis stok : 20"""
        barang = fetch_all("SELECT id, name, stock FROM items ORDER BY id")
        for row in barang:
            print(f'{row["name"]} stok : {int(row["stock"])}')

    def batal(self, nomor):
        """BONUS. Batalkan pembelian berdasarkan nomor pembelian. Cek berurutan:
        1. nomor bukan bilangan bulat 1 atau lebih, atau tidak ada -> "Pembelian tidak ditemukan"
        2. pembelian itu sudah dibatalkan                            -> "Pembelian sudah dibatalkan"
        Kalau lolos: pembelian ditandai batal, saldo siswa bertambah sebesar total yang
        dulu dibayar, dan stok barang bertambah sebesar jumlah yang dulu dibeli.
        Tidak mencetak apa pun."""
        nomor = self._bilangan_positif(nomor)
        if nomor is None:
            print("Pembelian tidak ditemukan")
            return

        pembelian = fetch_all(
            """
            SELECT p.id, p.student_id, p.item_id, p.qty, p.total, p.status
            FROM purchases p
            WHERE p.id = %s
            """,
            (nomor,),
        )
        if not pembelian:
            print("Pembelian tidak ditemukan")
            return

        pembelian = pembelian[0]
        if pembelian["status"] == "batal":
            print("Pembelian sudah dibatalkan")
            return

        execute(
            "UPDATE purchases SET status = 'batal' WHERE id = %s",
            (nomor,),
        )
        execute(
            "UPDATE students SET balance = balance + %s WHERE id = %s",
            (int(pembelian["total"]), pembelian["student_id"]),
        )
        execute(
            "UPDATE items SET stock = stock + %s WHERE id = %s",
            (int(pembelian["qty"]), pembelian["item_id"]),
        )
