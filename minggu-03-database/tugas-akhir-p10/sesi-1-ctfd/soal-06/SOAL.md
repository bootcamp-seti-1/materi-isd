# Soal 6 — Dua Jenis JOIN

**Tingkat:** Medium · **Poin:** 200
**Folder:** `~/seti-isd-materi/minggu-03-database/tugas-akhir/sesi-1-ctfd/soal-06`

**Cerita.** Mas Bayu menerima klien baru, Portal Alumni Kampus, yang belum punya satu tugas pun. Ia penasaran: kalau tugas digabung dengan proyeknya, apakah proyek baru itu muncul? Dimas menulis dua query untuk menjawabnya, satu memakai `JOIN` dan satu memakai `LEFT JOIN`.

**Bahan.** File `data.sql`, `query-a.sql`, dan `query-b.sql` (dua query Dimas). Bacalah isi kedua query itu.

**Langkah awal** (ganti `p00` dengan ID-mu, huruf kecil). Ketik di terminal Ubuntu, satu per satu:

```text
sudo service mysql start
cd ~/seti-isd-materi/minggu-03-database/tugas-akhir/sesi-1-ctfd/soal-06
mysql -u sakura_p00 -p sakura_db < data.sql
```

Perintah ini mereset data soal ke keadaan awal. Ulangi kapan saja kalau datanya sudah berubah. Password MySQL: `sakura123` (saat diketik tidak tampil di layar, itu normal).

Lalu jalankan dua query Dimas satu per satu:

```text
mysql -t -u sakura_p00 -p sakura_db < query-a.sql
mysql -t -u sakura_p00 -p sakura_db < query-b.sql
```

**Pertanyaan.** Berapa jumlah **baris** hasil `query-a.sql`, dan berapa jumlah baris hasil `query-b.sql`? (Hitung baris datanya saja, tidak termasuk baris judul kolom dan garis tabel.)

**Cara menjawab.** Tulis jumlah baris query A, koma, lalu jumlah baris query B, tanpa spasi. Contoh bentuknya: `5,6`. Kirim jawabannya ke CTFd.
