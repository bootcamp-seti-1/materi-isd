# Soal 9 — Barang Termurah

**Tingkat:** Hard · **Poin:** 300
**Folder:** `~/seti-isd-materi/minggu-05-backend/tugas-akhir/sesi-1-ctfd/soal-09`

**Cerita.** Dimas menambahkan endpoint `GET /v1/items/termurah` untuk menampilkan barang paling murah. Kodenya terlihat benar, tapi setiap kali dipanggil hasilnya error. Dimas menyerah dan menyerahkannya kepadamu.

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
curl -i http://localhost:8100/v1/items/termurah
```

**Pertanyaan.** Pertama, jalankan perintah di atas dan catat status code-nya. Kedua, cari penyebabnya di `server-soal/main.py` dan perbaiki **tanpa mengubah isi fungsi apa pun** (petunjuk: FastAPI mencocokkan alamat sesuai urutan endpoint ditulis). Simpan file, lalu jalankan perintah yang sama. Apa status code sebelum diperbaiki, dan apa nama barang termurah setelah diperbaiki?

**Cara menjawab.** Tulis status code sebelum diperbaiki, lalu nama barang, dipisah koma tanpa spasi setelah koma. Contoh bentuknya: `500,Buku Tulis`. Kirim jawabannya ke CTFd.
