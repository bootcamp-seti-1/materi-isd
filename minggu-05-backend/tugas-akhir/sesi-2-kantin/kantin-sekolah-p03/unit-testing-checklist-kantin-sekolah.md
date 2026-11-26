# Checklist Unit Testing API Menu & Pesanan

## Sebelum Mulai

Pastikan data awal berisi **6 menu**, lalu catat stok masing-masing
menu.

Tes yang mengubah data sebaiknya dilakukan secara berurutan. Untuk
mengulang pengujian dari awal, jalankan `db/schema.sql` lalu
`db/seed.sql` sesuai README.

> **Perhatian:** Perintah reset akan menghapus data uji.

## Menu

-   [ ] `GET /v1/menus` menampilkan 6 menu awal.
	- Curl
		- curl -X 'GET' \ 'http://127.0.0.1:8000/v1/menus?limit=10&offset=0' \ -H 'accept: */*'
	- Request URL
		- http://127.0.0.1:8000/v1/menus?limit=10&offset=0
	- Output:
		- [ { "id": 1, "name": "Nasi Goreng", "category": "makanan", "price": 12000, "stock": 20, "created_at": "2026-11-26T20:29:20" }, { "id": 2, "name": "Mi Ayam", "category": "makanan", "price": 10000, "stock": 15, "created_at": "2026-11-26T20:29:20" }, { "id": 3, "name": "Roti Bakar", "category": "makanan", "price": 8000, "stock": 0, "created_at": "2026-11-26T20:29:20" }, { "id": 4, "name": "Es Teh", "category": "minuman", "price": 3000, "stock": 50, "created_at": "2026-11-26T20:29:20" }, { "id": 5, "name": "Jus Jeruk", "category": "minuman", "price": 7000, "stock": 10, "created_at": "2026-11-26T20:29:20" }, { "id": 6, "name": "Air Mineral", "category": "minuman", "price": 4000, "stock": 30, "created_at": "2026-11-26T20:29:20" } ]
-   [ ] Filter kategori makanan/minuman dan pagination (`limit`,
    `offset`) memberikan hasil yang sesuai; kategori atau nilai
    agination yang tidak valid ditolak `422`.
-   [ ] `GET /v1/menus/9999` mengembalikan `404`.
-   [ ] `POST /v1/menus` dengan data valid mengembalikan `201`; spasi di
    nama dibuang dan stok yang tidak dikirim bernilai `0`.
-   [ ] Coba batas nama: 3 dan 50 karakter diterima; kurang dari 3,
    lebih dari 50, atau hanya spasi ditolak `422`.
-   [ ] Coba kategori tidak valid, harga di luar 1000--50000, harga
    bukan kelipatan 500, serta stok di luar 0--200: masing-masing
    ditolak `422`.
-   [ ] Kirim field tambahan yang tidak dikenal: ditolak `422`.
-   [ ] Buat nama yang sudah ada dengan kapitalisasi berbeda, misalnya
    `nasi goreng`: `409`, detail `Nama menu sudah ada`.
-   [ ] `PATCH` hanya mengubah field yang dikirim; field lain dan stok
    yang tidak diubah tetap sama.
-   [ ] `PATCH` menu yang tidak ada mengembalikan `404`.
-   [ ] Kirim `null` pada field PATCH: `422`. Uji juga ID menu tidak ada
    dengan body `null`; sesuai urutan aturan, hasilnya harus `404`.
-   [ ] Ubah nama menjadi nama menu lain, termasuk beda kapitalisasi:
    `409`, detail `Nama menu sudah ada`.
-   [ ] Mengirim nama menu itu sendiri sebagai nama baru tidak dianggap
    duplikat.

## Pesanan

-   [ ] Body pesanan dengan `menu_id <= 0`, `qty` di luar 1--10, atau
    field asing ditolak `422`.
-   [ ] Pesan menu yang tidak ada: `400`, detail `Menu tidak ditemukan`.
-   [ ] Pesan lebih banyak dari stok: `409`, detail `Stok tidak cukup`;
    pastikan stok dan jumlah pesanan tidak berubah.
-   [ ] Pesanan valid mengembalikan `201`, status `baru`, total yang
    benar, dan stok menu berkurang sesuai `qty`.
-   [ ] Uji subtotal di bawah ambang diskon dan tepat di ambang `50000`,
    misalnya harga `10000` × qty `5`: total harus `45000`. Uji juga di
    atas ambang, misalnya subtotal `70000`: total `63000`.
-   [ ] `GET /v1/orders/{id}` mengembalikan detail yang benar; ID yang
    tidak ada mengembalikan `404`.
-   [ ] Batalkan pesanan valid: status menjadi `batal` dan stok menu
    kembali bertambah sesuai qty pesanan.
-   [ ] Batalkan pesanan yang sama sekali lagi: `409`, detail
    `Pesanan sudah dibatalkan`; pastikan stok tidak bertambah lagi.
-   [ ] Batalkan pesanan yang tidak ada: `404`.

## Bonus

-   [ ] `GET /v1/orders` menampilkan semua pesanan berurutan berdasarkan
    ID.
-   [ ] Filter `?status=baru` dan `?status=batal` hanya menampilkan
    status yang diminta.
-   [ ] `GET /v1/laporan` hanya menghitung pesanan berstatus `baru`;
    pesanan batal tidak masuk hitungan pendapatan.
-   [ ] Saat belum ada pesanan baru, laporan mengembalikan
    `jumlah_pesanan: 0` dan `pendapatan: 0`.

## Catatan Validasi Error

Untuk error dengan pesan yang ditentukan README, cocokkan juga teks
`detail`-nya secara persis.
