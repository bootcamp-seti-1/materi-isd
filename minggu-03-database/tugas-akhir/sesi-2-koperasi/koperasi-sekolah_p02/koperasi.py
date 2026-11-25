from db import fetch_all, execute
import aturan


class Koperasi:
    def isi(self, nama, nominal):
        """Tambah saldo siswa. Cek berurutan:
        1. nama siswa tidak ada -> cetak "Siswa tidak ditemukan"
        2. nominal bukan bilangan bulat 1 atau lebih -> cetak "Nominal tidak valid"
        Kalau lolos, saldo siswa bertambah sebesar nominal. Tidak mencetak apa pun."""
        # TODO
        siswa = fetch_all(
            "SELECT id FROM students WHERE BINARY name = %s",
            (nama,)
        )
        if not siswa: 
            print("Siswa tidak ditemukan")
            return

        # Memisahkan try-except dan if itu seperti mengecek bentuk bendanya dulu sebelum mengecek ukuran/nilainya.
        try:
            jumlah = int(nominal)
        except ValueError:
            print("Nominal tidak valid")
            return

        if jumlah < 1:
            print("Nominal tidak valid")
            return

        execute(
                "UPDATE students SET balance = balance + %s WHERE id = %s",
                (jumlah, siswa[0]["id"]) # Ada tuple (kumpulan data berurutan yang tidak bisa diubah langsung) disini.
        )

    def saldo(self, nama):
        """Cetak satu baris:  Andi saldo : 30000
        Kalau nama siswa tidak ada, cetak "Siswa tidak ditemukan"."""
        # TODO
        siswa = fetch_all(
            "SELECT name, balance FROM students WHERE BINARY name = %s",
            (nama,)
        )
        if not siswa:
            print("Siswa tidak ditemukan")
            return

        print(f'{siswa[0]["name"]} saldo : {siswa[0]["balance"]}')

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
        siswa = fetch_all(
            "SELECT id, balance FROM students WHERE BINARY name = %s",
            (nama,)
            )
        if not siswa:
            print('Siswa tidak ditemukan')
            return

        daftar_barang = fetch_all(
            "SELECT id, price, stock FROM items WHERE BINARY name = %s",
            (barang,)
            )
        if not daftar_barang:
            print('Barang tidak ditemukan')
            return

        try:
            jumlah = int(jumlah)
        except ValueError:
            print('Jumlah tidak valid')
            return

        if jumlah < 1:
            print('Jumlah tidak valid')
            return

        pembelian_lama = fetch_all(
            "SELECT COALESCE(SUM(qty), 0) AS total_qty FROM purchases WHERE student_id = %s AND item_id = %s AND status = 'ok'",
            (siswa[0]["id"], daftar_barang[0]["id"])
            )

        jumlah_sebelumnya = pembelian_lama[0]["total_qty"]
        if jumlah_sebelumnya + jumlah > aturan.BATAS_PER_BARANG:
            print("Melebihi batas pembelian")
            return

        if daftar_barang[0]["stock"] < jumlah:
            print("Stok tidak cukup")
            return

        subtotal = daftar_barang[0]["price"] * jumlah
        diskon = 0

        if subtotal >= aturan.DISKON_MULAI:
            diskon = subtotal * aturan.DISKON_PERSEN // 100

        total_bayar = subtotal - diskon

        if siswa[0]["balance"] < total_bayar:
            print("Saldo tidak cukup")
            return

        execute(
            "UPDATE students SET balance = balance - %s WHERE id = %s",
            (total_bayar, siswa[0]["id"])
            )

        execute(
            "UPDATE items SET stock = stock - %s WHERE id = %s",
            (jumlah, daftar_barang[0]["id"])
            )

        execute(
            "INSERT INTO purchases (student_id, item_id, qty, total) VALUES (%s, %s, %s, %s)",
            (siswa[0]["id"], daftar_barang[0]["id"], jumlah, total_bayar)
            )

    def laporan(self):
        """Cetak satu baris per barang, urut dari pendapatan terbesar. Kalau pendapatan
        sama, urut nama barang dari A sampai Z. Barang yang belum terjual tetap dicetak:
            Pensil 3 buah pendapatan : 6000
        Pembelian yang dibatalkan tidak dihitung. Baris terakhir adalah jumlah semuanya:
            TOTAL 3 buah pendapatan : 6000"""
        # TODO
        data_barang = fetch_all(
            "SELECT i.id, i.name, COALESCE(SUM(p.qty), 0) AS jumlah, COALESCE(SUM(p.total), 0) AS pendapatan FROM items AS i LEFT JOIN purchases AS p ON p.item_id = i.id AND p.status = 'ok' GROUP BY i.id, i.name ORDER BY pendapatan DESC, i.name ASC"
            )

        jumlah_total = 0
        pendapatan_total = 0

        for barang in data_barang:
            jumlah = int(barang["jumlah"])
            pendapatan = int(barang["pendapatan"])

            print(
                f'{barang["name"]} {jumlah} buah '
                f'pendapatan : {pendapatan}'
            )

            jumlah_total += jumlah
            pendapatan_total += pendapatan

        print(
            f"TOTAL {jumlah_total} buah pendapatan : {pendapatan_total}"
        )

    def stok(self):
        """BONUS. Cetak satu baris per barang, urut sesuai nomor barang (id):
            Buku_Tulis stok : 20"""
        # TODO
        data_barang = fetch_all(
            "SELECT name, stock FROM items ORDER BY id"
        )

        for barang in data_barang:
            print(f'{barang["name"]} stok : {barang["stock"]}')


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

        pembelian = fetch_all(
            "SELECT id, student_id, item_id, qty, total, status FROM purchases WHERE id = %s",
            (nomor,)
        )

        if not pembelian:
            print("Pembelian tidak ditemukan")
            return

        if pembelian[0]["status"] == "batal":
            print("Pembelian sudah dibatalkan")
            return

        execute(
            "UPDATE purchases SET status = 'batal' WHERE id = %s",
            (nomor,)
        )

        execute(
            "UPDATE students SET balance = balance + %s WHERE id = %s",
            (pembelian[0]["total"], pembelian[0]["student_id"])
        )

        execute(
            "UPDATE items SET stock = stock + %s WHERE id = %s",
            (pembelian[0]["qty"], pembelian[0]["item_id"])
        )
