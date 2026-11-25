# Soal 4 — Halaman Kedua

**Tingkat:** Easy · **Poin:** 100
**Folder:** `~/seti-isd-materi/minggu-05-backend/tugas-akhir/sesi-1-ctfd/soal-04`

**Cerita.** Tim frontend membuat halaman katalog alat tulis (kategori `atk`) yang menampilkan 2 barang per halaman. Mereka ingin mengecek isi halaman kedua.

**Langkah awal: nyalakan server soal.** Buka terminal Ubuntu (Terminal 1), lalu ketik satu per satu:

```text
cd ~/seti-isd-materi/minggu-05-backend/tugas-akhir/sesi-1-ctfd/server-soal
```

```text
uv run fastapi dev main.py --port 8100
```

Biarkan Terminal 1 menyala. Ketik perintah `curl` di terminal lain (Terminal 2). Dokumentasi server ada di `http://localhost:8100/docs`.

Data server disimpan di memori. Kalau datanya sudah berubah karena soal lain, matikan server dengan `Ctrl+C` lalu jalankan lagi perintah di atas.

**Perintah:**

```text
curl -s "http://localhost:8100/v1/items?category=atk&limit=2&offset=2" | python3 -m json.tool
```

**Pertanyaan.** Jalankan perintah di atas. Barang apa saja yang tampil? Lihat `id`-nya.

**Cara menjawab.** Tulis `id` barang yang tampil, urut dari kecil ke besar, dipisah koma tanpa spasi. Contoh bentuknya: `10,11`. Kirim jawabannya ke CTFd.
