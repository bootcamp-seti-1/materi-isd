# Soal 9 — Mencari Tugas

**Tingkat:** Hard · **Poin:** 300
**Folder:** `~/latihan-python-h3/soal-09`

**Cerita.** Daftar tugas tim sudah belasan dan Mas Bayu sulit menemukan yang dia cari.
Dia minta perintah baru **`cari KATA`** yang menampilkan hanya tugas yang judulnya
mengandung kata itu. Ada dua syarat: huruf besar-kecil tidak dibedakan (`rapat`, `Rapat`,
dan `RAPAT` sama saja), dan nomor yang tampil harus tetap **nomor aslinya** di daftar
lengkap, bukan nomor baru dari 1.

**Bahan.** Folder ini berisi `tugas.py`, `main.py` (versi Hari 2), dan `masukan.txt`.

**Tugasmu.** Tambahkan method `cari` di `PengelolaTugas` dan cabang `cari KATA` di
`main.py`. Tiap tugas yang cocok dicetak dengan format yang sama seperti `list`
(`NOMOR. [x] JUDUL`). Kalau tidak ada yang cocok, cetak `Tidak ditemukan`.

Jalankan dengan `uv run main.py < masukan.txt`.

**Pertanyaan.** Pada perintah `cari rapat` di `masukan.txt`, tugas bernomor berapa saja
yang tampil?

**Cara menjawab.** Tulis nomor-nomornya dari yang terkecil, dipisah koma tanpa spasi. Contoh bentuknya: `2,6`. Kirim jawabannya ke CTFd.
