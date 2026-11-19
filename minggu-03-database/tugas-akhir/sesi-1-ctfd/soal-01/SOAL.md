# Soal 1 — Rekap Tugas Mas Bayu

**Tingkat:** Easy · **Poin:** 100
**Folder:** `~/seti-isd-materi/minggu-03-database/tugas-akhir/sesi-1-ctfd/soal-01`

**Cerita.** Mas Bayu bersiap rapat mingguan dan ingin tahu keadaan seluruh tugas timnya: berapa yang belum dikerjakan, berapa yang sedang dikerjakan, dan berapa yang sudah selesai.

**Bahan.** File `data.sql` (data tim Mas Bayu) dan `jawaban.sql` (tempat kamu menulis query).

**Langkah awal** (ganti `p00` dengan ID-mu, huruf kecil). Ketik di terminal Ubuntu, satu per satu:

```text
sudo service mysql start
cd ~/seti-isd-materi/minggu-03-database/tugas-akhir/sesi-1-ctfd/soal-01
mysql -u sakura_p00 -p sakura_db < data.sql
```

Perintah ini mereset data soal ke keadaan awal. Ulangi kapan saja kalau datanya sudah berubah. Password MySQL: `sakura123` (saat diketik tidak tampil di layar, itu normal).

Buka `jawaban.sql` di VS Code, tulis querymu di bawah komentarnya, simpan dengan `Ctrl+S`, lalu jalankan:

```text
mysql -t -u sakura_p00 -p sakura_db < jawaban.sql
```

**Pertanyaan.** Tulis satu perintah `SELECT` pada tabel `tasks` yang menghitung jumlah baris per `status` (pakai `COUNT(*)` dan `GROUP BY status`). Berapa jumlah tugas berstatus `todo`, `doing`, dan `done`?

**Cara menjawab.** Tulis tiga angka berurutan: jumlah `todo`, jumlah `doing`, lalu jumlah `done`, dipisah koma tanpa spasi. Contoh bentuknya: `1,2,3`. Kirim jawabannya ke CTFd.
