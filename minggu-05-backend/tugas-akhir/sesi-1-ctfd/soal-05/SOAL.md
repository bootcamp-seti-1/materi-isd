# Soal 5 — PATCH atau PUT

**Tingkat:** Medium · **Poin:** 200
**Folder:** `~/seti-isd-materi/minggu-05-backend/tugas-akhir/sesi-1-ctfd/soal-05`

**Cerita.** Harga Spidol Papan (barang nomor 4) naik menjadi 10000. Dimas mengubahnya dengan PATCH. Setelah itu Rani juga mengganti nama barangnya dengan PUT, tapi hanya mengirim nama dan harga. Besoknya stok di aplikasi kasir terlihat aneh.

**Langkah awal: nyalakan server soal.** Buka terminal Ubuntu (Terminal 1), lalu ketik satu per satu:

```text
cd ~/seti-isd-materi/minggu-05-backend/tugas-akhir/sesi-1-ctfd/server-soal
```

```text
uv run fastapi dev main.py --port 8100
```

Biarkan Terminal 1 menyala. Ketik perintah `curl` di terminal lain (Terminal 2). Dokumentasi server ada di `http://localhost:8100/docs`.

Data server disimpan di memori. Kalau datanya sudah berubah karena soal lain, matikan server dengan `Ctrl+C` lalu jalankan lagi perintah di atas.

Restart server dulu supaya datanya masih awal.

**Perintah:**

```text
curl -s -X PATCH http://localhost:8100/v1/items/4 -H "Content-Type: application/json" -d '{"price": 10000}'
curl -s -X PUT http://localhost:8100/v1/items/4 -H "Content-Type: application/json" -d '{"name": "Spidol Papan Biru", "price": 10000}'
```

**Pertanyaan.** Jalankan dua perintah di atas satu per satu, berurutan. Berapa `stock` barang nomor 4 setelah PATCH, dan berapa `stock` setelah PUT?

**Cara menjawab.** Tulis `stock` setelah PATCH, lalu `stock` setelah PUT, dipisah koma tanpa spasi. Contoh bentuknya: `7,7`. Kirim jawabannya ke CTFd.
