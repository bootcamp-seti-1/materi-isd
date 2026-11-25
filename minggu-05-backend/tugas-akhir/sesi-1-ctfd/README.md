# Sesi 1 — Kuis CTFd Backend API (60 menit)

10 soal, jawaban berupa teks pendek yang dikirim ke CTFd. Tiap soal punya foldernya sendiri berisi `SOAL.md` dan berkas pendukung. Sembilan soal memakai **server soal** (aplikasi FastAPI Toko Sakura di folder `server-soal`), satu soal memakai MySQL.

## Cara mengerjakan

1. Buka terminal Ubuntu (Terminal 1), lalu nyalakan server soal:

    ```text
    cd ~/seti-isd-materi/minggu-05-backend/tugas-akhir/sesi-1-ctfd/server-soal
    ```

    ```text
    uv run fastapi dev main.py --port 8100
    ```

2. Buka terminal kedua (Terminal 2) untuk mengetik perintah `curl`.
3. Buka `SOAL.md` di folder soal (mis. `soal-01`) di VS Code, baca ceritanya, lalu ikuti langkahnya.
4. Kirim jawaban ke CTFd, sesuai "Cara menjawab" di soal tersebut.

Server soal memakai port **8100**, bukan 8000. Kalau `sakura-api` milikmu masih menyala di port 8000, biarkan saja, tidak bentrok.

## Daftar soal

| No | Judul | Tingkat | Poin |
|----|-------|---------|------|
| 1 | Rak yang Tersembunyi | Easy | 100 |
| 2 | Barang Baru | Easy | 100 |
| 3 | Harga yang Aneh | Easy | 100 |
| 4 | Halaman Kedua | Easy | 100 |
| 5 | PATCH atau PUT | Medium | 200 |
| 6 | Versi Lama | Medium | 200 |
| 7 | Delapan Kiriman | Medium | 200 |
| 8 | Pencarian yang Bocor | Hard | 300 |
| 9 | Barang Termurah | Hard | 300 |
| 10 | PIN yang Terlihat | Hard | 300 |

## Aturan

- Boleh membuka lembar Hari 1 dan Hari 2, kode `sakura-api` milikmu, dan bertanya ke trainer.
- Data server soal disimpan di memori. Kalau datanya sudah berubah karena soal lain, restart server (`Ctrl+C`, lalu jalankan lagi).
- Jawaban salah boleh dicoba lagi, tapi jangan tebak-tebakan beruntun.
