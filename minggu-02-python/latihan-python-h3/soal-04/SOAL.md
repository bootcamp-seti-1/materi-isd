# Soal 4 — Perintah undone

**Tingkat:** Medium · **Poin:** 200
**Folder:** `~/latihan-python-h3/soal-04`

**Cerita.** Dimas kebablasan: dia menandai tiga tugas selesai padahal salah satunya
belum. Di `sakura-tasks` belum ada cara membatalkan tanda selesai. Mas Bayu minta
perintah baru bernama **`undone NOMOR`**, kebalikan dari `done NOMOR`.

**Bahan.** Folder ini berisi `tugas.py` (class `Tugas` dan `PengelolaTugas`, sama seperti
Hari 2), `main.py`, dan `masukan.txt` (ketikan Mas Bayu untuk mencoba).

**Tugasmu.** Tambahkan perintah `undone NOMOR`:
- Kalau nomor benar dan tugasnya sudah selesai: tandainya jadi belum selesai, lalu cetak
  `Dibatalkan: JUDUL`.
- Kalau nomor benar tapi tugasnya memang belum selesai: cetak `Belum selesai: JUDUL`,
  tanpa mengubah apa pun.
- Kalau nomor di luar daftar: cetak `Nomor tidak ada`.
- Kalau yang diketik setelah `undone ` bukan angka: cetak `Nomor harus angka`.

`masukan.txt` sengaja berisi ketikan yang salah (nomor tidak ada dan nomor bukan angka).
Programmu **tidak boleh berhenti karena error**. Ia harus mencetak pesan yang sesuai lalu
lanjut ke perintah berikutnya.

Kamu perlu menyentuh `tugas.py` dan `main.py`. Jalankan dengan
`uv run main.py < masukan.txt`.

**Pertanyaan.** Setelah seluruh isi `masukan.txt` dijalankan dengan programmu, ada dua hal
yang perlu kamu baca dari layar: (1) baris `stats`, yaitu `Total … | selesai … | belum …`
(ambil angka `selesai` dan angka `belum`), dan (2) judul tugas yang muncul pada pesan
`Belum selesai: JUDUL`.

**Cara menjawab.** Tulis tiga bagian berurutan, dipisah koma tanpa spasi: angka `selesai`, angka `belum`, lalu judul tugasnya persis seperti yang tercetak (huruf kecil semua). Contoh bentuknya: `1,3,rapat pagi`. Kirim jawabannya ke CTFd.
