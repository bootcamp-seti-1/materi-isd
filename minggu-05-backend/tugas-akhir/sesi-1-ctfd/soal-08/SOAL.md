# Soal 8 — Pencarian yang Bocor

**Tingkat:** Hard · **Poin:** 300
**Folder:** `~/seti-isd-materi/minggu-05-backend/tugas-akhir/sesi-1-ctfd/soal-08`

**Cerita.** Toko A memakai fitur pencarian produk buatan vendor lama. Fitur itu seharusnya hanya menampilkan produk milik Toko A. Seorang pengguna iseng mengetik `x' OR '1'='1` di kotak pencarian, dan layar menampilkan produk yang seharusnya tidak boleh ia lihat.

**Bahan.** File `cari.py` (kode pencarian vendor lama, tidak perlu dijalankan) dan `data.sql`.

**Langkah awal** (ganti `p00` dengan ID-mu, huruf kecil). Ketik di terminal Ubuntu, satu per satu:

```text
sudo service mysql start
```

```text
cd ~/seti-isd-materi/minggu-05-backend/tugas-akhir/sesi-1-ctfd/soal-08
```

```text
mysql -u sakura_p00 -p sakura_db < data.sql
```

Password MySQL: `sakura123`.

**Perintah:**

```text
mysql -u sakura_p00 -p sakura_db
```

**Pertanyaan.** Baca fungsi `cari_produk` di `cari.py`. Susun sendiri teks SQL yang terbentuk kalau `nama` berisi `x' OR '1'='1` (persis, termasuk tanda kutipnya), lalu ketik SQL itu di `mysql>` dan akhiri dengan `;`. Berapa baris yang tampil, dan dari berapa toko yang berbeda?

**Cara menjawab.** Tulis jumlah baris, lalu jumlah toko berbeda, dipisah koma tanpa spasi. Contoh bentuknya: `5,1`. Kirim jawabannya ke CTFd.
