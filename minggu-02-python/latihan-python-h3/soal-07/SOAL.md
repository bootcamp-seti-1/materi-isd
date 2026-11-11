# Soal 7 — Tugas Prioritas

**Tingkat:** Medium · **Poin:** 200
**Folder:** `~/latihan-python-h3/soal-07`

**Cerita.** Mas Bayu ingin tahu mana tugas yang genting. Dia minta tiap tugas punya
**prioritas**: biasanya `biasa`, tapi bisa ditandai `tinggi` kalau mendesak. Daftar tugas
juga harus menampilkan prioritasnya di ujung baris.

**Bahan.** Folder ini berisi `tugas.py`, `main.py` (versi Hari 2), dan `masukan.txt`.

**Tugasmu.**
1. Class `Tugas` menerima prioritas. Kalau tidak diisi, nilainya `biasa`. Tampilan satu tugas
   menjadi `[ ] judul (prioritas)` atau `[x] judul (prioritas)`.
2. `PengelolaTugas.tambah` ikut menerima prioritas (default `biasa`). Pesan
   `Ditambahkan: JUDUL` tidak berubah.
3. Di `main.py`, perintah baru **`add! JUDUL`** menambah tugas dengan prioritas `tinggi`.
   Perintah `add JUDUL` yang lama tetap membuat tugas `biasa`.

Jalankan dengan `uv run main.py < masukan.txt`.

**Pertanyaan.** Setelah `masukan.txt` dijalankan, tulis baris **ketiga** dari hasil `list`,
persis seperti yang tercetak di layar.

**Cara menjawab.** Tulis satu baris itu persis, termasuk nomor, kurung, dan spasi. Salin dari layar supaya tidak salah ketik. Kirim jawabannya ke CTFd.
