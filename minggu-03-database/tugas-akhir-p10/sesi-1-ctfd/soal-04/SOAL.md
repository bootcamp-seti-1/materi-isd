# Soal 4 — Tugas Prioritas Dua

**Tingkat:** Easy · **Poin:** 100
**Folder:** `~/seti-isd-materi/minggu-03-database/tugas-akhir/sesi-1-ctfd/soal-04`

**Cerita.** Mas Bayu ingin melihat tugas yang belum dikerjakan dan berprioritas biasa (prioritas 2), supaya bisa membaginya ke tim. Ia juga ingin tahu tenggat paling dekat di antara tugas-tugas itu.

**Bahan.** File `data.sql` dan `jawaban.sql` (tempat kamu menulis query).

**Langkah awal** (ganti `p00` dengan ID-mu, huruf kecil). Ketik di terminal Ubuntu, satu per satu:

```text
sudo service mysql start
cd ~/seti-isd-materi/minggu-03-database/tugas-akhir/sesi-1-ctfd/soal-04
mysql -u sakura_p00 -p sakura_db < data.sql
```

Perintah ini mereset data soal ke keadaan awal. Ulangi kapan saja kalau datanya sudah berubah. Password MySQL: `sakura123` (saat diketik tidak tampil di layar, itu normal).

Buka `jawaban.sql`, tulis querymu, simpan dengan `Ctrl+S`, lalu jalankan:

```text
mysql -t -u sakura_p00 -p sakura_db < jawaban.sql
```

**Pertanyaan.** Tulis satu perintah `SELECT` pada tabel `tasks` dengan dua syarat sekaligus: `status` berisi `todo`, **dan** `priority` berisi `2`. Tampilkan kolom `title` dan `due_date`, diurutkan dari `due_date` terlama ke terbaru. Berapa jumlah barisnya, dan berapa tanggal `due_date` yang paling awal?

**Cara menjawab.** Tulis jumlah baris, koma, lalu tanggalnya (bentuk `TAHUN-BULAN-TANGGAL`), tanpa spasi. Contoh bentuknya: `9,2026-01-01`. Kirim jawabannya ke CTFd.
