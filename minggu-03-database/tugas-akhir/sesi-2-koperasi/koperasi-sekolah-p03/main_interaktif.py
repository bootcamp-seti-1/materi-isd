from koperasi import Koperasi


def tampilkan_header():
    print("=" * 55)
    print("SISTEM KOPERASI BERJALAN - SIAP MENERIMA PERINTAH")
    print("=" * 55)
    print("Fitur & format input yang harus dimasukkan:")
    print("  1. saldo <nama_siswa>                -> cek saldo")
    print("  2. isi <nama_siswa> <nominal>        -> tambah saldo (angka >= 1)")
    print("  3. beli <nama_siswa> <barang> <jml>  -> beli barang (jml angka >= 1)")
    print("  4. laporan                           -> rekap penjualan & total")
    print("  5. stok                              -> cek sisa stok barang")
    print("  6. batal <nomor_pembelian>           -> batalkan transaksi (angka >= 1)")
    print("  7. exit                              -> keluar dari program")
    print("Catatan: gunakan '_' untuk nama ber-spasi (cth: Buku_Tulis).")
    print("-" * 55)


def jalankan():
    koperasi = Koperasi()
    tampilkan_header()

    while True:
        try:
            baris = input("> ")
        except EOFError:
            print("\nProgram selesai.")
            break

        kata = baris.split()
        if not kata:
            print("[Info] Input kosong. Ketik perintah sesuai daftar di atas.")
            continue

        perintah = kata[0]

        if perintah == "laporan":
            if len(kata) == 1:
                koperasi.laporan()
            else:
                print("[Input salah] Perintah 'laporan' tidak butuh argumen. Gunakan: laporan")

        elif perintah == "stok":
            if len(kata) == 1:
                koperasi.stok()
            else:
                print("[Input salah] Perintah 'stok' tidak butuh argumen. Gunakan: stok")

        elif perintah == "saldo":
            if len(kata) == 2:
                koperasi.saldo(kata[1])
            else:
                print("[Input salah] Format 'saldo' harus 2 kata. Gunakan: saldo <nama_siswa>")

        elif perintah == "batal":
            if len(kata) == 2:
                koperasi.batal(kata[1])
            else:
                print("[Input salah] Format 'batal' harus 2 kata. Gunakan: batal <nomor_pembelian>")

        elif perintah == "isi":
            if len(kata) == 3:
                koperasi.isi(kata[1], kata[2])
            else:
                print("[Input salah] Format 'isi' harus 3 kata. Gunakan: isi <nama_siswa> <nominal>")

        elif perintah == "beli":
            if len(kata) == 4:
                koperasi.beli(kata[1], kata[2], kata[3])
            else:
                print("[Input salah] Format 'beli' harus 4 kata. Gunakan: beli <nama_siswa> <barang> <jumlah>")
        elif perintah == "exit":
            print("Program selesai.")
            break
        else:
            print(
                f"[Input salah] Perintah '{perintah}' tidak dikenal. "
                "Gunakan salah satu: saldo, isi, beli, laporan, stok, batal."
            )


if __name__ == "__main__":
    jalankan()