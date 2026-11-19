# Soal 8 — COUNT yang Berbohong

**Tingkat:** Hard · **Poin:** 300
**Folder:** `~/seti-isd-materi/minggu-03-database/tugas-akhir/sesi-1-ctfd/soal-08`

**Cerita.** Mas Bayu ingin melihat tiap proyek beserta jumlah tugas yang sudah selesai. Dimas membuat dua query yang hampir sama. Bedanya hanya satu: query A memakai `COUNT(t.id)`, query B memakai `COUNT(*)`. Mas Bayu bingung kenapa angkanya berbeda, padahal proyek yang sama.

**Bahan.** File `data.sql` (sudah berisi proyek baru tersebut), `query-a.sql`, dan `query-b.sql`. Bacalah kedua query itu dengan teliti, termasuk bagian `ON`.

**Langkah awal** (ganti `p00` dengan ID-mu, huruf kecil). Ketik di terminal Ubuntu, satu per satu:

```text
sudo service mysql start
cd ~/seti-isd-materi/minggu-03-database/tugas-akhir/sesi-1-ctfd/soal-08
mysql -u sakura_p00 -p sakura_db < data.sql
```

Perintah ini mereset data soal ke keadaan awal. Ulangi kapan saja kalau datanya sudah berubah. Password MySQL: `sakura123` (saat diketik tidak tampil di layar, itu normal).

Lalu jalankan dua query Dimas satu per satu:

```text
mysql -t -u sakura_p00 -p sakura_db < query-a.sql
mysql -t -u sakura_p00 -p sakura_db < query-b.sql
```

**Pertanyaan.** Untuk tiap query, jumlahkan semua angka di kolom `jumlah` (semua baris). Berapa jumlahnya untuk query A, dan berapa untuk query B?

**Cara menjawab.** Tulis jumlah query A, koma, lalu jumlah query B, tanpa spasi. Contoh bentuknya: `3,5`. Kirim jawabannya ke CTFd.
