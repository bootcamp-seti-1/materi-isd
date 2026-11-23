from db import fetch_all, execute
import aturan


def _parse_positif(teks):
    s = str(teks)
    if not s.isdigit():
        return None
    angka = int(s)
    return angka if angka >= 1 else None


class Koperasi:
    def _cari_siswa(self, nama):
        rows = fetch_all(
            "SELECT id, name, balance FROM students WHERE BINARY name = %s",
            (nama,),
        )
        return rows[0] if rows else None

    def _cari_barang(self, nama):
        rows = fetch_all(
            "SELECT id, name, price, stock FROM items WHERE BINARY name = %s",
            (nama,),
        )
        return rows[0] if rows else None

    def isi(self, nama, nominal):
        siswa = self._cari_siswa(nama)
        if siswa is None:
            print("Siswa tidak ditemukan")
            return
        angka = _parse_positif(nominal)
        if angka is None:
            print("Nominal tidak valid")
            return
        execute(
            "UPDATE students SET balance = balance + %s WHERE id = %s",
            (angka, siswa["id"]),
        )

    def saldo(self, nama):
        siswa = self._cari_siswa(nama)
        if siswa is None:
            print("Siswa tidak ditemukan")
            return
        print(f"{siswa['name']} saldo : {siswa['balance']}")

    def beli(self, nama, barang, jumlah):
        siswa = self._cari_siswa(nama)
        if siswa is None:
            print("Siswa tidak ditemukan")
            return

        item = self._cari_barang(barang)
        if item is None:
            print("Barang tidak ditemukan")
            return

        qty = _parse_positif(jumlah)
        if qty is None:
            print("Jumlah tidak valid")
            return

        sudah_beli = fetch_all(
            """
            SELECT COALESCE(SUM(qty), 0) AS total_qty
            FROM purchases
            WHERE student_id = %s AND item_id = %s AND status = 'ok'
            """,
            (siswa["id"], item["id"]),
        )[0]["total_qty"]

        if int(sudah_beli) + qty > aturan.BATAS_PER_BARANG:
            print("Melebihi batas pembelian")
            return

        if item["stock"] < qty:
            print("Stok tidak cukup")
            return

        subtotal = item["price"] * qty
        if subtotal >= aturan.DISKON_MULAI:
            total_bayar = subtotal - (subtotal * aturan.DISKON_PERSEN // 100)
        else:
            total_bayar = subtotal

        if siswa["balance"] < total_bayar:
            print("Saldo tidak cukup")
            return

        execute(
            "UPDATE students SET balance = balance - %s WHERE id = %s",
            (total_bayar, siswa["id"]),
        )
        execute(
            "UPDATE items SET stock = stock - %s WHERE id = %s",
            (qty, item["id"]),
        )
        execute(
            """
            INSERT INTO purchases (student_id, item_id, qty, total, status)
            VALUES (%s, %s, %s, %s, 'ok')
            """,
            (siswa["id"], item["id"], qty, total_bayar),
        )

    def laporan(self):
        rows = fetch_all(
            """
            SELECT i.name,
                   COALESCE(SUM(p.qty), 0) AS terjual,
                   COALESCE(SUM(p.total), 0) AS pendapatan
            FROM items i
            LEFT JOIN purchases p ON p.item_id = i.id AND p.status = 'ok'
            GROUP BY i.id, i.name
            ORDER BY pendapatan DESC, i.name ASC
            """
        )
        total_qty = 0
        total_pendapatan = 0
        for r in rows:
            qty = int(r["terjual"])
            pend = int(r["pendapatan"])
            total_qty += qty
            total_pendapatan += pend
            print(f"{r['name']} {qty} buah pendapatan : {pend}")
        print(f"TOTAL {total_qty} buah pendapatan : {total_pendapatan}")

    def stok(self):
        rows = fetch_all("SELECT name, stock FROM items ORDER BY id ASC")
        for r in rows:
            print(f"{r['name']} stok : {r['stock']}")

    def batal(self, nomor):
        id_beli = _parse_positif(nomor)
        if id_beli is None:
            print("Pembelian tidak ditemukan")
            return

        rows = fetch_all(
            "SELECT id, student_id, item_id, qty, total, status FROM purchases WHERE id = %s",
            (id_beli,),
        )
        if not rows:
            print("Pembelian tidak ditemukan")
            return

        beli = rows[0]
        if beli["status"] == "batal":
            print("Pembelian sudah dibatalkan")
            return

        execute(
            "UPDATE purchases SET status = 'batal' WHERE id = %s",
            (beli["id"],),
        )
        execute(
            "UPDATE students SET balance = balance + %s WHERE id = %s",
            (beli["total"], beli["student_id"]),
        )
        execute(
            "UPDATE items SET stock = stock + %s WHERE id = %s",
            (beli["qty"], beli["item_id"]),
        )
