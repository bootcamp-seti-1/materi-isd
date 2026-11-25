from db import fetch_all, execute
import aturan


def _bulat_positif(teks):
    """Cek apakah teks adalah bilangan bulat >= 1."""
    try:
        n = int(teks)
    except (TypeError, ValueError):
        return None
    if n < 1:
        return None
    return n


class Koperasi:
    def isi(self, nama, nominal):
        """Tambah saldo siswa."""
        siswa = fetch_all("SELECT id FROM students WHERE name = %s", (nama,))
        if not siswa:
            print("Siswa tidak ditemukan")
            return
        n = _bulat_positif(nominal)
        if n is None:
            print("Nominal tidak valid")
            return
        execute("UPDATE students SET balance = balance + %s WHERE name = %s",
                (n, nama))

    def saldo(self, nama):
        """Cetak saldo siswa."""
        siswa = fetch_all("SELECT balance FROM students WHERE name = %s", (nama,))
        if not siswa:
            print("Siswa tidak ditemukan")
            return
        print(f"{nama} saldo : {siswa[0]['balance']}")

    def beli(self, nama, barang, jumlah):
        """Siswa membeli barang."""
        # 1. siswa ada?
        siswa = fetch_all("SELECT id, balance FROM students WHERE name = %s", (nama,))
        if not siswa:
            print("Siswa tidak ditemukan")
            return
        siswa = siswa[0]

        # 2. barang ada?
        item = fetch_all("SELECT id, price, stock FROM items WHERE name = %s", (barang,))
        if not item:
            print("Barang tidak ditemukan")
            return
        item = item[0]

        # 3. jumlah valid?
        qty = _bulat_positif(jumlah)
        if qty is None:
            print("Jumlah tidak valid")
            return

        # 4. batas pembelian per barang (hanya yang tidak dibatalkan)
        sudah = fetch_all(
            "SELECT COALESCE(SUM(qty), 0) AS total FROM purchases "
            "WHERE student_id = %s AND item_id = %s AND status = 'ok'",
            (siswa['id'], item['id'])
        )[0]['total']
        if sudah + qty > aturan.BATAS_PER_BARANG:
            print("Melebihi batas pembelian")
            return

        # 5. stok cukup?
        if item['stock'] < qty:
            print("Stok tidak cukup")
            return

        # 6. saldo cukup?
        subtotal = item['price'] * qty
        if subtotal >= aturan.DISKON_MULAI:
            total = subtotal - (subtotal * aturan.DISKON_PERSEN // 100)
        else:
            total = subtotal
        if siswa['balance'] < total:
            print("Saldo tidak cukup")
            return

        # Lolos: update saldo, stok, catat pembelian
        execute("UPDATE students SET balance = balance - %s WHERE id = %s",
                (total, siswa['id']))
        execute("UPDATE items SET stock = stock - %s WHERE id = %s",
                (qty, item['id']))
        execute("INSERT INTO purchases (student_id, item_id, qty, total) "
                "VALUES (%s, %s, %s, %s)",
                (siswa['id'], item['id'], qty, total))

    def laporan(self):
        """Cetak laporan penjualan tiap barang."""
        rows = fetch_all(
            "SELECT i.name AS name, "
            "       COALESCE(SUM(CASE WHEN p.status='ok' THEN p.qty ELSE 0 END), 0) AS qty, "
            "       COALESCE(SUM(CASE WHEN p.status='ok' THEN p.total ELSE 0 END), 0) AS pendapatan "
            "FROM items i "
            "LEFT JOIN purchases p ON p.item_id = i.id "
            "GROUP BY i.id, i.name "
            "ORDER BY pendapatan DESC, i.name ASC"
        )
        total_qty = 0
        total_pend = 0
        for r in rows:
            print(f"{r['name']} {r['qty']} buah pendapatan : {r['pendapatan']}")
            total_qty += r['qty']
            total_pend += r['pendapatan']
        print(f"TOTAL {total_qty} buah pendapatan : {total_pend}")

    def stok(self):
        """BONUS: cetak stok tiap barang urut id."""
        rows = fetch_all("SELECT name, stock FROM items ORDER BY id ASC")
        for r in rows:
            print(f"{r['name']} stok : {r['stock']}")

    def batal(self, nomor):
        """BONUS: batalkan pembelian."""
        n = _bulat_positif(nomor)
        if n is None:
            print("Pembelian tidak ditemukan")
            return
        rows = fetch_all(
            "SELECT id, student_id, item_id, qty, total, status "
            "FROM purchases WHERE id = %s", (n,)
        )
        if not rows:
            print("Pembelian tidak ditemukan")
            return
        p = rows[0]
        if p['status'] == 'batal':
            print("Pembelian sudah dibatalkan")
            return
        execute("UPDATE purchases SET status = 'batal' WHERE id = %s", (n,))
        execute("UPDATE students SET balance = balance + %s WHERE id = %s",
                (p['total'], p['student_id']))
        execute("UPDATE items SET stock = stock + %s WHERE id = %s",
                (p['qty'], p['item_id']))