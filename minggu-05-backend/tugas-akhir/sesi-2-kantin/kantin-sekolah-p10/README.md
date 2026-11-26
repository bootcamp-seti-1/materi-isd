# Sesi 2 — API Kantin Sekolah

Waktu: **60 menit**. Boleh memakai AI dan internet. Pahami kode yang kamu kumpulkan, karena trainer akan menanyaimu.

Penilaian dan peringkat: skenario yang lulus paling banyak menang. Kalau jumlahnya sama, yang **waktu commit terakhirnya lebih awal** menang. Hasil akhir wajib sudah di-push ke GitHub sebelum batas waktu yang diumumkan trainer.

**Penting: sesi ini dikerjakan di branch milikmu sendiri, bernama `kantin-pXX` (contoh: `kantin-p03`). Jangan push ke `main`.** Dengan begitu pekerjaanmu tidak bisa tertimpa pekerjaan teman, dan sebaliknya.

## Ceritanya

Bu Siti mengelola kantin SD Harapan. Tahun depan sekolah ingin siswa memesan makanan lewat aplikasi HP, supaya antrean saat istirahat tidak panjang. Tim frontend sudah siap membuat aplikasinya, tapi mereka butuh API dulu. Mas Bayu memberimu tugas: buat API kantin yang menyimpan datanya di MySQL. Tabel, data awal, dan kerangka kodenya sudah disiapkan. Kamu mengisi aturan validasi dan endpoint yang belum jadi.

## Cara mulai

**Ketik di terminal** (ganti `p00` dengan ID-mu, huruf kecil), satu per satu:

```text
sudo service mysql start
```

```text
cd ~/seti-isd-materi/minggu-05-backend/tugas-akhir/sesi-2-kantin
```

```text
git switch main
```

```text
git pull
```

Buat branch milikmu sendiri dan langsung pindah ke sana (ganti `p00` dengan ID-mu):

```text
git switch -c kantin-p00
```

Cek bahwa kamu sudah berada di branch yang benar:

```text
git branch
```

**Yang harus muncul di layar:** ada tanda `*` di depan `kantin-p00`. Kalau tanda `*` masih di depan `main`, ulangi perintah `git switch -c kantin-p00`. Kalau muncul `already exists`, pakai `git switch kantin-p00` (tanpa `-c`).

```text
cp -r kantin-sekolah kantin-sekolah-p00
```

```text
cd kantin-sekolah-p00
```

```text
cp .env.example .env
```

```text
code .
```

Di VS Code, buka `.env`, ganti `sakura_p00` dengan ID-mu dan `ganti_dengan_password` dengan `sakura123`, lalu simpan. Folder `kantin-sekolah` (tanpa ID) adalah contoh asli: **jangan diubah**. Kerjakan hanya di folder yang ada ID-mu.

Buat tabel kantin dan isi data awalnya (ganti `p00` dengan ID-mu, password `sakura123`):

```text
mysql -u sakura_p00 -p sakura_db < db/schema.sql
```

```text
mysql -u sakura_p00 -p sakura_db < db/seed.sql
```

Nyalakan server di **Terminal 1**:

```text
uv run --env-file .env fastapi dev main.py
```

Buka `http://localhost:8000/docs` di browser. Kalau halaman dokumentasi muncul dan `GET /v1/menus` mengembalikan 6 menu, semuanya sudah tersambung. Endpoint yang belum dibuat akan mengembalikan status `501`. Itu normal.

## Data awal

Tabel `kantin_menus`:

| id | name | category | price | stock |
| --- | --- | --- | --- | --- |
| 1 | Nasi Goreng | makanan | 12000 | 20 |
| 2 | Mi Ayam | makanan | 10000 | 15 |
| 3 | Roti Bakar | makanan | 8000 | 0 |
| 4 | Es Teh | minuman | 3000 | 50 |
| 5 | Jus Jeruk | minuman | 7000 | 10 |
| 6 | Air Mineral | minuman | 4000 | 30 |

Tabel `kantin_orders` awalnya kosong. Kolomnya: `id`, `menu_id`, `qty`, `total`, `status` (`baru` atau `batal`, bawaan `baru`), `created_at`.

## Endpoint

| Method | Path | Keadaan |
| --- | --- | --- |
| `GET` | `/v1/menus` | Sudah jadi. Filter `category`, pagination `limit` (1 sampai 50, bawaan 10) dan `offset` |
| `GET` | `/v1/menus/{menu_id}` | Sudah jadi. `404` kalau tidak ada |
| `POST` | `/v1/menus` | **Buat.** Menambah menu |
| `PATCH` | `/v1/menus/{menu_id}` | **Buat.** Mengubah sebagian isi menu |
| `POST` | `/v1/orders` | **Buat.** Membuat pesanan |
| `GET` | `/v1/orders/{order_id}` | **Buat.** Detail pesanan |
| `POST` | `/v1/orders/{order_id}/batal` | **Buat.** Membatalkan pesanan |
| `GET` | `/v1/orders` | **Bonus.** Daftar pesanan, filter `status` |
| `GET` | `/v1/laporan` | **Bonus.** Ringkasan penjualan |

Semua response sukses berbentuk seperti model `Menu`, `Order`, dan `Laporan` di `schemas.py`. Semua response error berbentuk `{"detail": "..."}`. Kalau ada pesan yang ditentukan di bawah, tulis **persis sama**.

## Aturan menu (POST dan PATCH `/v1/menus`)

Tambahkan aturan ini di `MenuCreate` dan `MenuUpdate` (`schemas.py`). Angkanya ambil dari `aturan.py`, jangan ditulis langsung.

| Field | Aturan |
| --- | --- |
| `name` | Spasi di awal dan akhir dibuang. Setelah itu panjangnya 3 sampai 50 huruf |
| `category` | Hanya `makanan` atau `minuman` |
| `price` | 1000 sampai 50000, dan harus kelipatan 500 (`11000` boleh, `11250` tidak) |
| `stock` | 0 sampai 200. Kalau tidak dikirim saat POST, isinya 0 |
| field lain | Field yang tidak dikenal ditolak |

Data yang melanggar aturan di atas ditolak dengan status `422`. Aturan ini dicek otomatis oleh Pydantic **lebih dulu**, sebelum pengecekan berurutan di bawah.

**POST `/v1/menus`:**

1. Kalau sudah ada menu dengan nama yang sama: `409` dengan pesan `Nama menu sudah ada`. Huruf besar dan kecil dianggap sama (`nasi goreng` sama dengan `Nasi Goreng`).
2. Kalau lolos: simpan, lalu kembalikan menu yang baru dibuat dengan status `201`.

**PATCH `/v1/menus/{menu_id}`:** pengecekan berurutan.

1. Menu tidak ada: `404`.
2. Ada field yang dikirim bernilai `null`: `422`.
3. `name` baru sama dengan nama menu **lain**: `409` dengan pesan `Nama menu sudah ada`.
4. Kalau lolos: ubah hanya field yang dikirim, lalu kembalikan menu dengan status `200`.

## Aturan pesanan (POST `/v1/orders`)

Body: `{"menu_id": 4, "qty": 2}`. `menu_id` harus lebih dari 0, `qty` 1 sampai 10, field lain ditolak. Pelanggaran aturan ini: `422`.

Pengecekan berurutan. Berhenti di kegagalan pertama, dan tidak ada data yang berubah.

| Urutan | Kejadian | Status | Pesan |
| --- | --- | --- | --- |
| 1 | Menu tidak ada | `400` | `Menu tidak ditemukan` |
| 2 | Stok menu kurang dari `qty` | `409` | `Stok tidak cukup` |

Cara menghitung `total`:

- Subtotal = harga menu × `qty`.
- Kalau subtotal **mencapai** 50000 atau lebih, total dipotong 10%.
- Hasilnya bilangan bulat (contoh: subtotal `70000`, total `63000`).

Kalau lolos: stok menu berkurang sebesar `qty`, pesanan disimpan dengan status `baru`, lalu kembalikan pesanan itu dengan status `201`.

## Aturan detail dan pembatalan

**GET `/v1/orders/{order_id}`:** `404` kalau tidak ada.

**POST `/v1/orders/{order_id}/batal`:** pengecekan berurutan.

1. Pesanan tidak ada: `404`.
2. Pesanan sudah berstatus `batal`: `409` dengan pesan `Pesanan sudah dibatalkan`.
3. Kalau lolos: status menjadi `batal`, stok menu bertambah sebesar `qty` pesanan itu, lalu kembalikan pesanan dengan status `200`.

## Aturan bonus

- `GET /v1/orders`: semua pesanan urut `id`. Kalau ada `?status=batal` atau `?status=baru`, tampilkan yang statusnya cocok saja.
- `GET /v1/laporan`: `{"jumlah_pesanan": 2, "pendapatan": 69000}`. Hanya pesanan berstatus `baru` yang dihitung. Kalau belum ada pesanan, keduanya `0`.

## File yang kamu kerjakan

| File | Keadaan | Tugasmu |
| --- | --- | --- |
| `schemas.py` | model masukan tanpa aturan | Tambahkan aturan di `MenuCreate`, `MenuUpdate`, `OrderCreate` |
| `routers/menus.py` | GET sudah jadi | Isi `buat_menu` dan `ubah_menu` |
| `routers/orders.py` | kerangka | Isi semua fungsi bertanda `TODO` |
| `main.py`, `aturan.py`, `db.py`, `db/` | sudah jadi | Jangan diubah |
| `.env` | kamu isi sendiri | Jangan di-push |

Waktu penilaian, `main.py`, `aturan.py`, `db.py`, dan folder `db` diganti dengan versi asli. Hanya `schemas.py`, `routers/`, dan file tambahan buatanmu yang dipakai.

## Memeriksa pekerjaanmu

Tidak ada alat cek otomatis. Kamu sendiri yang memastikan API-mu sesuai aturan di atas, dengan `curl` di Terminal 2 atau tombol **Try it out** di `/docs`. Penilaian memakai banyak skenario yang tidak diperlihatkan, jadi coba sebanyak mungkin kasus: yang berhasil, yang harus ditolak, dan urutan pengecekannya.

Contoh bentuk perintah `curl`:

```text
curl -s http://localhost:8000/v1/menus/4 | python3 -m json.tool
```

```text
curl -i -X POST http://localhost:8000/v1/orders -H "Content-Type: application/json" -d '{"menu_id": 4, "qty": 2}'
```

Setiap kali kamu mencoba POST, PATCH, atau batal, data di database ikut berubah. Untuk mengembalikan data kantin ke keadaan awal (6 menu, belum ada pesanan), jalankan dari folder `kantin-sekolah-p00` (ganti `p00` dengan ID-mu):

```text
mysql -u sakura_p00 -p sakura_db < db/schema.sql
```

```text
mysql -u sakura_p00 -p sakura_db < db/seed.sql
```

Penilaian selalu dimulai dari data awal ini.

## Mengumpulkan

Semua perintah di bawah dikerjakan di branch `kantin-p00` milikmu (ganti `p00` dengan ID-mu).

**Ketik di terminal:**

```text
cd ~/seti-isd-materi
```

```text
git branch
```

Pastikan tanda `*` ada di depan `kantin-p00`, **bukan** di depan `main`. Kalau masih di `main`, jangan lanjut: panggil trainer.

```text
git status
```

Pastikan `.env` **tidak** ada di daftar, dan hanya folder `kantin-sekolah-p00` milikmu yang berubah. Lalu:

```text
git add minggu-05-backend/tugas-akhir/sesi-2-kantin/kantin-sekolah-p00
```

```text
git commit -m "Sesi 2: API kantin sekolah"
```

Push **pertama kali** (membuat branch-mu di GitHub):

```text
git push -u origin kantin-p00
```

Push **berikutnya** cukup:

```text
git push
```

Tidak perlu `git pull --rebase`, karena branch ini hanya kamu yang memakai. Buka repo di GitHub, pilih branch `kantin-p00` di tombol pilihan branch, dan pastikan folder `kantin-sekolah-p00` ada di sana.

Boleh commit dan push berkali-kali setiap ada kemajuan. Yang dihitung untuk peringkat adalah waktu commit **terakhir** di branch-mu.

### Setelah sesi selesai

Kembali ke `main` supaya materi pertemuan berikutnya bisa di-pull seperti biasa:

```text
git switch main
```

Folder `kantin-sekolah-p00` akan hilang dari laptopmu saat berada di `main`. Itu normal: pekerjaanmu aman di branch `kantin-p00`, dan kembali lagi kalau kamu menjalankan `git switch kantin-p00`.
