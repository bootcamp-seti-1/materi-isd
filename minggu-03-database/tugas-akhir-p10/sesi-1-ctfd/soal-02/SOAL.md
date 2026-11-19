# Soal 2 — Data yang Ditolak

**Tingkat:** Easy · **Poin:** 100
**Folder:** `~/seti-isd-materi/minggu-03-database/tugas-akhir/sesi-1-ctfd/soal-02`

**Cerita.** Rani, anak magang, mencoba memasukkan tugas untuk proyek nomor 999. Padahal proyek itu tidak ada. MySQL menolaknya dan menampilkan pesan error yang diawali sebuah angka. Mas Bayu ingin angka itu dicatat di buku catatan tim.

**Bahan.** File `data.sql` dan `coba.sql` (berisi perintah `INSERT` milik Rani).

**Langkah awal** (ganti `p00` dengan ID-mu, huruf kecil). Ketik di terminal Ubuntu, satu per satu:

```text
sudo service mysql start
cd ~/seti-isd-materi/minggu-03-database/tugas-akhir/sesi-1-ctfd/soal-02
mysql -u sakura_p00 -p sakura_db < data.sql
```

Perintah ini mereset data soal ke keadaan awal. Ulangi kapan saja kalau datanya sudah berubah. Password MySQL: `sakura123` (saat diketik tidak tampil di layar, itu normal).

Jalankan perintah Rani:

```text
mysql -u sakura_p00 -p sakura_db < coba.sql
```

**Pertanyaan.** MySQL menampilkan tulisan `ERROR` diikuti sebuah angka dalam kurung (sebelum tanda `(`). Berapa angka itu?

**Cara menjawab.** Tulis angkanya saja. Contoh bentuknya: `9999`. Kirim jawabannya ke CTFd.
