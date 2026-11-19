# Soal 10 — Menghapus Proyek

**Tingkat:** Hard · **Poin:** 300
**Folder:** `~/seti-isd-materi/minggu-03-database/tugas-akhir/sesi-1-ctfd/soal-10`

**Cerita.** Klien membatalkan proyek Toko Online Kopi Nusantara. Mas Bayu menyuruh Rani menghapusnya dari database. MySQL menolak perintahnya dan menampilkan error. Rani panik, lalu bertanya padamu. Kamu harus menemukan kenapa ditolak dan cara menghapusnya dengan benar.

**Bahan.** File `data.sql`, `hapus-proyek.sql` (perintah pertama Rani), dan `hapus-tugas.sql` (langkah berikutnya).

**Langkah awal** (ganti `p00` dengan ID-mu, huruf kecil). Ketik di terminal Ubuntu, satu per satu:

```text
sudo service mysql start
cd ~/seti-isd-materi/minggu-03-database/tugas-akhir/sesi-1-ctfd/soal-10
mysql -u sakura_p00 -p sakura_db < data.sql
```

Perintah ini mereset data soal ke keadaan awal. Ulangi kapan saja kalau datanya sudah berubah. Password MySQL: `sakura123` (saat diketik tidak tampil di layar, itu normal).

Jalankan perintah pertama Rani, lalu baca pesan errornya:

```text
mysql -u sakura_p00 -p sakura_db < hapus-proyek.sql
```

Lalu masuk ke MySQL supaya jumlah baris yang terhapus tampil:

```text
mysql -u sakura_p00 -p sakura_db
```

Ketik di `mysql>`:

```text
SOURCE hapus-tugas.sql;
```

**Pertanyaan.** Ada dua hal yang perlu kamu baca dari layar: (1) angka setelah tulisan `ERROR` saat menjalankan `hapus-proyek.sql`, dan (2) jumlah baris yang terhapus (`rows affected`) saat menjalankan `hapus-tugas.sql`.

**Cara menjawab.** Tulis angka error, koma, lalu jumlah baris yang terhapus, tanpa spasi. Contoh bentuknya: `1234,5`. Kirim jawabannya ke CTFd.
