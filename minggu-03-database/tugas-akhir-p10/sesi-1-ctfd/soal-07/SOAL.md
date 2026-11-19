# Soal 7 — Data yang Hilang

**Tingkat:** Medium · **Poin:** 200
**Folder:** `~/seti-isd-materi/minggu-03-database/tugas-akhir/sesi-1-ctfd/soal-07`

**Cerita.** Tim Mas Bayu memakai aplikasi `sakura-tasks`. Mereka menambah tugas baru, daftar tugas menampilkannya, dan semuanya tampak normal. Tapi setelah aplikasi ditutup lalu dibuka lagi, tugas baru itu hilang dari database. Dimas yakin penyebabnya ada di fungsi `execute` di `db.py`, karena ada satu baris yang terhapus tanpa sengaja.

**Bahan.** File `db.py` di folder ini. Kodenya tidak perlu dijalankan. Bacalah dan bandingkan dengan `db.py` yang kamu buat di Hari 2.

**Langkah awal** (ganti `p00` dengan ID-mu, huruf kecil). Ketik di terminal Ubuntu, satu per satu:

```text
sudo service mysql start
cd ~/seti-isd-materi/minggu-03-database/tugas-akhir/sesi-1-ctfd/soal-07
mysql -u sakura_p00 -p sakura_db < data.sql
```

Perintah ini mereset data soal ke keadaan awal. Ulangi kapan saja kalau datanya sudah berubah. Password MySQL: `sakura123` (saat diketik tidak tampil di layar, itu normal).

**Pertanyaan.** Perintah apa yang hilang dari fungsi `execute`, yang membuat perubahan tidak tersimpan di database?

**Cara menjawab.** Tulis nama perintahnya saja, huruf kecil, tanpa tanda kurung dan tanpa awalan `conn.`. Contoh bentuknya: `nama_perintah`. Kirim jawabannya ke CTFd.
