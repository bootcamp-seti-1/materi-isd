# Soal 7 — Delapan Kiriman

**Tingkat:** Medium · **Poin:** 200
**Folder:** `~/seti-isd-materi/minggu-05-backend/tugas-akhir/sesi-1-ctfd/soal-07`

**Cerita.** Tim frontend mengirim delapan contoh data barang baru dan bertanya: mana yang akan diterima API, dan mana yang ditolak? Mereka tidak mau menebak, jadi kamu diminta mencobanya satu per satu.

**Langkah awal: nyalakan server soal.** Buka terminal Ubuntu (Terminal 1), lalu ketik satu per satu:

```text
cd ~/seti-isd-materi/minggu-05-backend/tugas-akhir/sesi-1-ctfd/server-soal
```

```text
uv run fastapi dev main.py --port 8100
```

Biarkan Terminal 1 menyala. Ketik perintah `curl` di terminal lain (Terminal 2). Dokumentasi server ada di `http://localhost:8100/docs`.

Data server disimpan di memori. Kalau datanya sudah berubah karena soal lain, matikan server dengan `Ctrl+C` lalu jalankan lagi perintah di atas.

**Bahan.** File `kiriman.txt` di folder soal ini berisi delapan perintah `curl`, bernomor 1 sampai 8.

**Perintah:**

```text
cat ~/seti-isd-materi/minggu-05-backend/tugas-akhir/sesi-1-ctfd/soal-07/kiriman.txt
```

**Pertanyaan.** Jalankan kedelapan perintah di `kiriman.txt`. Kiriman nomor berapa saja yang diterima dengan status `201`?

**Cara menjawab.** Tulis nomor kiriman yang diterima, urut dari kecil ke besar, dipisah koma tanpa spasi. Contoh bentuknya: `2,4,8`. Kirim jawabannya ke CTFd.
