# Soal 9 — Syarat di Tempat yang Salah

**Tingkat:** Hard · **Poin:** 300
**Folder:** `~/seti-isd-materi/minggu-03-database/tugas-akhir/sesi-1-ctfd/soal-09`

**Cerita.** Mas Bayu ingin melihat **semua proyek** beserta jumlah tugas selesainya, termasuk proyek yang belum punya tugas selesai (angkanya 0). Dimas membuat dua versi query. Versi A menaruh syarat `status = 'done'` di `ON`. Versi B menaruhnya di `WHERE`. Hanya salah satu yang menampilkan semua proyek.

**Bahan.** File `data.sql` (sudah berisi proyek baru tersebut), `query-a.sql`, dan `query-b.sql`.

**Langkah awal** (ganti `p00` dengan ID-mu, huruf kecil). Ketik di terminal Ubuntu, satu per satu:

```text
sudo service mysql start
cd ~/seti-isd-materi/minggu-03-database/tugas-akhir/sesi-1-ctfd/soal-09
mysql -u sakura_p00 -p sakura_db < data.sql
```

Perintah ini mereset data soal ke keadaan awal. Ulangi kapan saja kalau datanya sudah berubah. Password MySQL: `sakura123` (saat diketik tidak tampil di layar, itu normal).

Lalu jalankan dua query Dimas satu per satu:

```text
mysql -t -u sakura_p00 -p sakura_db < query-a.sql
mysql -t -u sakura_p00 -p sakura_db < query-b.sql
```

**Pertanyaan.** Berapa jumlah **baris** hasil query A, dan berapa jumlah baris hasil query B? (Hitung baris datanya saja, tidak termasuk baris judul kolom dan garis tabel.)

**Cara menjawab.** Tulis jumlah baris query A, koma, lalu jumlah baris query B, tanpa spasi. Contoh bentuknya: `5,3`. Kirim jawabannya ke CTFd.
