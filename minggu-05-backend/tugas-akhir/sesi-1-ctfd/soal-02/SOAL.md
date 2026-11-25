# Soal 2 — Barang Baru

**Tingkat:** Easy · **Poin:** 100
**Folder:** `~/seti-isd-materi/minggu-05-backend/tugas-akhir/sesi-1-ctfd/soal-02`

**Cerita.** Toko Sakura mulai menjual Pensil 2B. Rani menambahkannya lewat API dengan mengirim nama dan harga saja, tanpa menyebut stok.

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
curl -i -X POST http://localhost:8100/v1/items -H "Content-Type: application/json" -d '{"name": "Pensil 2B", "price": 3000}'
```

**Pertanyaan.** Jalankan perintah di atas. Berapa status code response-nya, dan berapa nilai `stock` barang baru itu?

**Cara menjawab.** Tulis status code, lalu nilai `stock`, dipisah koma tanpa spasi. Contoh bentuknya: `200,5`. Kirim jawabannya ke CTFd.
