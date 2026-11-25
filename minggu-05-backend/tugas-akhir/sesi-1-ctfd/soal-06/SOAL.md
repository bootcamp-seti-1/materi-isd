# Soal 6 — Versi Lama

**Tingkat:** Medium · **Poin:** 200
**Folder:** `~/seti-isd-materi/minggu-05-backend/tugas-akhir/sesi-1-ctfd/soal-06`

**Cerita.** Server Toko Sakura masih menyimpan endpoint PATCH versi lama di alamat `/v1/lama/items/{item_id}`, buatan anak magang sebelum ada review kode. Kasir mengeluh: setelah harga diubah lewat endpoint itu, beberapa data barang hilang.

**Langkah awal: nyalakan server soal.** Buka terminal Ubuntu (Terminal 1), lalu ketik satu per satu:

```text
cd ~/seti-isd-materi/minggu-05-backend/tugas-akhir/sesi-1-ctfd/server-soal
```

```text
uv run fastapi dev main.py --port 8100
```

Biarkan Terminal 1 menyala. Ketik perintah `curl` di terminal lain (Terminal 2). Dokumentasi server ada di `http://localhost:8100/docs`.

Data server disimpan di memori. Kalau datanya sudah berubah karena soal lain, matikan server dengan `Ctrl+C` lalu jalankan lagi perintah di atas.

Restart server dulu supaya datanya masih awal. Setelah soal ini selesai, restart lagi, karena data barang nomor 4 menjadi rusak.

**Perintah:**

```text
curl -s -X PATCH http://localhost:8100/v1/lama/items/4 -H "Content-Type: application/json" -d '{"price": 9500}' | python3 -m json.tool
```

**Pertanyaan.** Jalankan perintah di atas, lalu bandingkan kode fungsi `ubah_item_versi_lama` dengan `ubah_item` di `server-soal/main.py`. Pada response, berapa field yang nilainya menjadi `null`?

**Cara menjawab.** Tulis jumlahnya saja. Contoh bentuknya: `9`. Kirim jawabannya ke CTFd.
