# Soal 3 — Kolom Penghubung

**Tingkat:** Easy · **Poin:** 100
**Folder:** `~/seti-isd-materi/minggu-03-database/tugas-akhir/sesi-1-ctfd/soal-03`

**Cerita.** Mas Bayu bertanya, "Bagaimana MySQL tahu tugas ini milik proyek yang mana?" Jawabannya ada di rancangan tabel `tasks`.

**Bahan.** File `data.sql`. Bacalah bagian `CREATE TABLE tasks` di dalamnya. Kamu juga boleh melihat rancangan tabelnya dengan perintah `DESCRIBE tasks;` di dalam `mysql>`.

**Langkah awal** (ganti `p00` dengan ID-mu, huruf kecil). Ketik di terminal Ubuntu, satu per satu:

```text
sudo service mysql start
cd ~/seti-isd-materi/minggu-03-database/tugas-akhir/sesi-1-ctfd/soal-03
mysql -u sakura_p00 -p sakura_db < data.sql
```

Perintah ini mereset data soal ke keadaan awal. Ulangi kapan saja kalau datanya sudah berubah. Password MySQL: `sakura123` (saat diketik tidak tampil di layar, itu normal).

**Pertanyaan.** Satu kolom di tabel `tasks` dipakai untuk menunjuk ke tabel `projects` (kolom itu memakai `FOREIGN KEY`). Apa nama kolomnya?

**Cara menjawab.** Tulis nama kolomnya saja, huruf kecil, persis seperti tertulis di tabel. Contoh bentuknya: `nama_kolom`. Kirim jawabannya ke CTFd.
