from db import fetch_all, execute
import aturan


class Koperasi:
    def isi(self, nama, nominal):
        """Tambah saldo siswa. Cek berurutan:
        1. nama siswa tidak ada -> cetak "Siswa tidak ditemukan"
        2. nominal bukan bilangan bulat 1 atau lebih -> cetak "Nominal tidak valid"
        Kalau lolos, saldo siswa bertambah sebesar nominal. Tidak mencetak apa pun."""
        # TODO
        pass

    def saldo(self, nama):
        """Cetak satu baris:  Andi saldo : 30000
        Kalau nama siswa tidak ada, cetak "Siswa tidak ditemukan"."""
        # TODO
        pass

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
        pass

    def laporan(self):
        """Cetak satu baris per barang, urut dari pendapatan terbesar. Kalau pendapatan
        sama, urut nama barang dari A sampai Z. Barang yang belum terjual tetap dicetak:
            Pensil 3 buah pendapatan : 6000
        Pembelian yang dibatalkan tidak dihitung. Baris terakhir adalah jumlah semuanya:
            TOTAL 3 buah pendapatan : 6000"""
        # TODO
        pass

    def stok(self):
        """BONUS. Cetak satu baris per barang, urut sesuai nomor barang (id):
            Buku_Tulis stok : 20"""
        # TODO
        pass

    def batal(self, nomor):
        """BONUS. Batalkan pembelian berdasarkan nomor pembelian. Cek berurutan:
        1. nomor bukan bilangan bulat 1 atau lebih, atau tidak ada -> "Pembelian tidak ditemukan"
        2. pembelian itu sudah dibatalkan                            -> "Pembelian sudah dibatalkan"
        Kalau lolos: pembelian ditandai batal, saldo siswa bertambah sebesar total yang
        dulu dibayar, dan stok barang bertambah sebesar jumlah yang dulu dibeli.
        Tidak mencetak apa pun."""
        # TODO
        pass
