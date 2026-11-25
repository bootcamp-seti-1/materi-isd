from db import fetch_all, execute
import aturan


class Koperasi:
    @staticmethod
    def _query_check(rows :list, message :str) -> bool :
        if not rows :
            print(message)
            return False
        return True

    @staticmethod
    def _parse_positive_int(value) -> int | None:
        if not isinstance(value, str) or not value.isdigit():
            return None
        parsed = int(value)
        return parsed if parsed >= 1 else None
    
    def isi(self, nama, nominal) -> None:
        """Tambah saldo siswa. Cek berurutan:
        1. nama siswa tidak ada -> cetak "Siswa tidak ditemukan"
        2. nominal bukan bilangan bulat 1 atau lebih -> cetak "Nominal tidak valid"
        Kalau lolos, saldo siswa bertambah sebesar nominal. Tidak mencetak apa pun."""

        fetch = fetch_all("SELECT name FROM students WHERE name = %s", (nama,))
        # Cek nama
        if not self._query_check(fetch, "Siswa tidak ditemukan") :
            return
        # Old name check
        # if len(fetch) < 1:
        #     print("Siswa tidak ditemukan")
        #     return

        # Cek nominal
        jumlah = self._parse_positive_int(nominal)
        if jumlah == None:
            print("Nominal tidak valid")
            return

        # Old positive int check
        # if not isinstance(nominal, str) or not nominal.isdigit():
        #     print("Nominal tidak valid")
        #     return
        
        # # Convert to int and check range
        # nominal = int(nominal)
        # if nominal < 1:
        #     print("Nominal tidak valid")
        #     return
        
        # Execute update on balance
        execute(
            "UPDATE students SET balance = balance + %s WHERE name = %s",
            (jumlah, nama),
        )

    def saldo(self, nama) -> None:
        """Cetak satu baris:  Andi saldo : 30000
        Kalau nama siswa tidak ada, cetak "Siswa tidak ditemukan"."""
        
        rows = fetch_all("SELECT balance FROM students WHERE name = %s", (nama,))
        if not rows:
            print("Siswa tidak ditemukan")
            return
        
        # fetch into rows = List['column_name']
        saldo = rows[0]['balance']
            
        # Print saldo
        print(nama, "saldo :", saldo)   

    def beli(self, nama, barang, jumlah) -> None:
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
        # Gerbang 1 : Nama valid
        siswa = fetch_all("SELECT * FROM students WHERE name = %s", (nama,))
        if not self._query_check(siswa, "Siswa tidak ditemukan") :
            return
        # Gerbang 2 : Load Toko
        fetch_toko = fetch_all("SELECT * FROM items")
        barang_toko = {item["name"]: item for item in fetch_toko}
        if barang not in barang_toko:
            print("Barang tidak ditemukan")
            return
        # Spesifik step 3
        jumlah = self._parse_positive_int(jumlah)
        if jumlah is None:
            print("Jumlah tidak valid")
            return
        # Load purchases
        id_siswa :int = siswa[0]['id']
        id_barang :int = barang_toko[barang]['id']
        fetch_barang_dibeli = fetch_all(
            "SELECT COALESCE(SUM(qty), 0) AS bought FROM purchases WHERE item_id = %s AND student_id = %s AND status = 'ok'",
            (id_barang, id_siswa)
            )
        
        # Step 4 - batas beli
        if fetch_barang_dibeli[0]["bought"] + jumlah > aturan.BATAS_PER_BARANG:
            print("Melebihi batas pembelian")
            return
        # Step 5 - cek stok
        if jumlah > barang_toko[barang]['stock']:
            print("Stok tidak cukup")
            return

        # Prepare final payment
        total_payment = barang_toko[barang]['price'] * jumlah
        if total_payment >= aturan.DISKON_MULAI:
            total_payment = (total_payment * (100 - aturan.DISKON_PERSEN)) // 100
        # Step 6 - saldo
        if siswa[0]['balance'] < total_payment:
            print("Saldo tidak cukup")
            return

        # Success
        # Update balance
        execute(
            "UPDATE students SET balance = balance - %s WHERE id = %s",
            (total_payment, id_siswa),
        )
        # Update shop item
        execute(
            "UPDATE items SET stock = stock - %s WHERE id = %s",
            (jumlah, id_barang),
        )
        # Add purchase history
        execute(
            "INSERT INTO purchases (student_id, item_id, qty, total, status) VALUES (%s, %s, %s, %s, %s)",
            (id_siswa, id_barang, jumlah, total_payment, "ok"),
        )

    def laporan(self) -> None:
        """Cetak satu baris per barang, urut dari pendapatan terbesar. Kalau pendapatan
        sama, urut nama barang dari A sampai Z. Barang yang belum terjual tetap dicetak:
            Pensil 3 buah pendapatan : 6000
        Pembelian yang dibatalkan tidak dihitung. Baris terakhir adalah jumlah semuanya:
            TOTAL 3 buah pendapatan : 6000"""

        rows = fetch_all("""
SELECT
items.name AS barang,
COALESCE(SUM(purchases.qty), 0) AS jumlah,
COALESCE(SUM(purchases.total), 0) AS pendapatan
FROM items
LEFT JOIN purchases
ON items.id = purchases.item_id AND purchases.status = 'ok'
GROUP BY items.id, items.name
ORDER BY pendapatan DESC, items.name ASC""")

        total_barang = 0
        total_pendapatan = 0

        for row in rows:
            jumlah = row["jumlah"] or 0
            pendapatan = row["pendapatan"] or 0

            print(row["barang"], jumlah, "buah pendapatan :", pendapatan)

            total_barang += jumlah
            total_pendapatan += pendapatan

        print("TOTAL", total_barang, "buah pendapatan :", total_pendapatan)

    def stok(self) -> None:
        """BONUS. Cetak satu baris per barang, urut sesuai nomor barang (id):
            Buku_Tulis stok : 20"""
        fetch_toko = fetch_all("SELECT name, stock from items ORDER BY id ASC")
        for i in fetch_toko:
            print(i['name'], "stok :", i['stock'])

    def batal(self, nomor) -> None:
        """BONUS. Batalkan pembelian berdasarkan nomor pembelian. Cek berurutan:
        1. nomor bukan bilangan bulat 1 atau lebih, atau tidak ada -> "Pembelian tidak ditemukan"
        2. pembelian itu sudah dibatalkan                            -> "Pembelian sudah dibatalkan"
        Kalau lolos: pembelian ditandai batal, saldo siswa bertambah sebesar total yang
        dulu dibayar, dan stok barang bertambah sebesar jumlah yang dulu dibeli.
        Tidak mencetak apa pun."""
        nomor = self._parse_positive_int(nomor)
        if nomor is None:
            print("Pembelian tidak ditemukan")
            return
        
        fetch_pembelian = fetch_all("SELECT * FROM purchases WHERE id = %s", (nomor,))
        if not self._query_check(fetch_pembelian, "Pembelian tidak ditemukan"):
            return
        if fetch_pembelian[0]['status'] == 'batal':
            print("Pembelian sudah dibatalkan")
            return

        jumlah = fetch_pembelian[0]['qty']
        payback = fetch_pembelian[0]['total']
        student_id = fetch_pembelian[0]['student_id']
        barang_id = fetch_pembelian[0]['item_id']

        execute("UPDATE purchases SET status = 'batal' WHERE id = %s", (nomor,))
        execute("UPDATE items SET stock = stock + %s WHERE id = %s", (jumlah, barang_id))
        execute("UPDATE students SET balance = balance + %s WHERE id = %s", (payback, student_id))