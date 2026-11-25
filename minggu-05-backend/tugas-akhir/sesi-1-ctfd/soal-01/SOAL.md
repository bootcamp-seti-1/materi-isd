# Soal 1 — Rak yang Tersembunyi

**Tingkat:** Easy · **Poin:** 100
**Folder:** `~/seti-isd-materi/minggu-05-backend/tugas-akhir/sesi-1-ctfd/soal-01`

**Cerita.** Bu Wati, petugas gudang Toko Sakura, ingin tahu letak rak barang nomor 3 (Penghapus). Dimas bilang letak rak tidak ada di body JSON, tapi tetap dikirim server di bagian lain response.

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
curl -i http://localhost:8100/v1/items/3
```

**Pertanyaan.** Jalankan perintah di atas. Response punya satu header yang namanya diawali `x-lokasi`. Apa isi header itu?

**Cara menjawab.** Tulis isi header-nya saja, persis seperti tampil. Contoh bentuknya: `Z-00`. Kirim jawabannya ke CTFd.
