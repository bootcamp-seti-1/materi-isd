# Soal 3 — Perintah update

**Tingkat:** Medium · **Poin:** 200
**Folder:** `~/latihan-python-h3/soal-03`

**Cerita.** Dimas sering salah ketik judul tugas di `sakura-tasks`, dan satu-satunya cara
membetulkannya sekarang adalah menambah tugas baru. Mas Bayu minta perintah baru bernama
**`update NOMOR JUDUL_BARU`** untuk mengganti judul tugas yang sudah ada. Programnya adalah
versi akhir Hari 1 (satu file `main.py`, gaya prosedural).

**Bahan.** Folder ini berisi `main.py` dan `masukan.txt` (ketikan Mas Bayu untuk mencoba,
satu perintah per baris).

**Tugasmu.** Tambahkan perintah `update NOMOR JUDUL_BARU`. Contoh: `update 2 laporan bulanan`
mengganti judul tugas nomor 2 menjadi `laporan bulanan`. Aturannya, dicek dari atas ke bawah:
- Kalau `NOMOR` bukan angka: cetak `Nomor harus angka`.
- Kalau nomor di luar daftar (0 atau lebih besar dari jumlah tugas): cetak `Nomor tidak ada`.
- Kalau judul barunya kosong, atau hanya berisi spasi, atau tidak diketik sama sekali: cetak
  `Judul tidak boleh kosong`.
- Kalau semuanya benar: ganti judulnya, lalu cetak `Diubah: JUDUL_LAMA -> JUDUL_BARU`.

Hanya judulnya yang berubah. Status selesai atau belum tidak boleh ikut berubah.

`masukan.txt` sengaja berisi ketikan yang salah (nomor bukan angka, nomor tidak ada, judul
kosong). Programmu **tidak boleh berhenti karena error**. Ia harus mencetak pesan yang sesuai
lalu lanjut ke perintah berikutnya. Jalankan dengan:

```text
uv run main.py < masukan.txt
```

**Pertanyaan.** Setelah seluruh isi `masukan.txt` dijalankan dengan programmu, perhatikan hasil
perintah `list` terakhir. Apa bunyi baris **kedua**-nya, persis seperti yang tercetak?

**Cara menjawab.** Tulis satu baris itu persis, termasuk nomor, titik, kurung, dan spasi. Salin dari layar supaya tidak salah ketik. Kirim jawabannya ke CTFd.
