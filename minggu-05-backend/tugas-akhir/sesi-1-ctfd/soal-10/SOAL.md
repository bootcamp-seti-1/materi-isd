# Soal 10 — PIN yang Terlihat

**Tingkat:** Hard · **Poin:** 300
**Folder:** `~/seti-isd-materi/minggu-05-backend/tugas-akhir/sesi-1-ctfd/soal-10`

**Cerita.** Toko Sakura punya program anggota. Setiap anggota punya PIN rahasia untuk membayar. Dimas yakin API-nya aman, karena daftar anggota di `GET /v1/members` hanya menampilkan `id` dan `name`. Mas Bayu memintamu membuktikan apakah itu benar.

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
curl -s http://localhost:8100/v1/members | python3 -m json.tool
```

**Pertanyaan.** Periksa semua endpoint anggota di `/docs` atau di `server-soal/main.py`. Ada satu endpoint yang lupa memakai `response_model`. Berapa PIN anggota bernama Rina?

**Cara menjawab.** Tulis PIN-nya saja. Contoh bentuknya: `0000`. Kirim jawabannya ke CTFd.
