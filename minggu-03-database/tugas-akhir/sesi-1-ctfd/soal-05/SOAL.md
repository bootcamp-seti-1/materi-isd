# Soal 5 — Lupa WHERE

**Tingkat:** Medium · **Poin:** 200
**Folder:** `~/seti-isd-materi/minggu-03-database/tugas-akhir/sesi-1-ctfd/soal-05`

**Cerita.** Rani ingin menjadikan satu tugas berprioritas 1. Tapi ia lupa menulis `WHERE`, jadi perintahnya mengenai seluruh tabel. MySQL tetap menjalankannya tanpa bertanya, lalu melaporkan dua angka: berapa baris yang cocok dengan syarat, dan berapa baris yang benar-benar berubah.

**Bahan.** File `data.sql` dan `coba.sql` (berisi perintah Rani).

**Langkah awal** (ganti `p00` dengan ID-mu, huruf kecil). Ketik di terminal Ubuntu, satu per satu:

```text
sudo service mysql start
cd ~/seti-isd-materi/minggu-03-database/tugas-akhir/sesi-1-ctfd/soal-05
mysql -u sakura_p00 -p sakura_db < data.sql
```

Perintah ini mereset data soal ke keadaan awal. Ulangi kapan saja kalau datanya sudah berubah. Password MySQL: `sakura123` (saat diketik tidak tampil di layar, itu normal).

Perintah ini harus dijalankan dari dalam MySQL supaya kedua angka itu tampil. Ketik di terminal:

```text
mysql -u sakura_p00 -p sakura_db
```

Lalu ketik di `mysql>`:

```text
SOURCE coba.sql;
```

**Pertanyaan.** Di bawah tulisan `Query OK` ada baris `Rows matched: … Changed: … Warnings: …`. Berapa angka `Rows matched` dan angka `Changed`? Pikirkan juga kenapa keduanya bisa berbeda.

**Cara menjawab.** Tulis angka `Rows matched`, koma, lalu angka `Changed`, tanpa spasi. Contoh bentuknya: `3,1`. Kirim jawabannya ke CTFd.
