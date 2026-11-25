# Soal 3 — Harga yang Aneh

**Tingkat:** Easy · **Poin:** 100
**Folder:** `~/seti-isd-materi/minggu-05-backend/tugas-akhir/sesi-1-ctfd/soal-03`

**Cerita.** Anak magang mengisi harga Stabilo dengan tulisan `murah`. API menolaknya dengan status 422 dan pesan error panjang. Mas Bayu ingin tahu, menurut pesan error itu, bagian mana yang salah.

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
curl -s -X POST http://localhost:8100/v1/items -H "Content-Type: application/json" -d '{"name": "Stabilo", "price": "murah"}' | python3 -m json.tool
```

**Pertanyaan.** Jalankan perintah di atas. Di dalam `detail`, ada `loc` yang berisi daftar dua teks. Apa isi `loc` itu?

**Cara menjawab.** Tulis kedua teks berurutan, dipisah koma tanpa spasi, tanpa tanda kutip. Contoh bentuknya: `query,limit`. Kirim jawabannya ke CTFd.
