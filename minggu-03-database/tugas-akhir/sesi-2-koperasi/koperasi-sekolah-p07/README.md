# Sesi 2 — Koperasi Sekolah

Waktu: **60 menit**. Boleh memakai AI dan internet. Pahami kode yang kamu kumpulkan, karena trainer akan menanyaimu.

Penilaian dan peringkat: skenario yang lulus paling banyak menang. Kalau jumlahnya sama, yang **waktu commit terakhirnya lebih awal** menang. Hasil akhir wajib sudah di-push ke GitHub **paling lambat Minggu, 22 November 2026, pukul 23.59**. Hasilnya dibahas hari Senin.

## Ceritanya

Bu Ratna mengelola koperasi SD Harapan. Selama ini ia mencatat saldo siswa dan penjualan alat tulis di buku tulis, dan sering salah hitung. Mas Bayu memberimu tugas: buat program koperasi yang menyimpan datanya di MySQL. Tabel, data awal, dan kerangka kodenya sudah disiapkan. Kamu mengisi logikanya.

## Cara mulai

**Ketik di terminal** (ganti `p00` dengan ID-mu, huruf kecil), satu per satu:

```text
sudo service mysql start
```

```text
cd ~/seti-isd-materi/minggu-03-database/tugas-akhir/sesi-2-koperasi
```

```text
git pull
```

```text
cp -r koperasi-sekolah koperasi-sekolah-p00
```

```text
cd koperasi-sekolah-p00
```

```text
code .
```

Di VS Code, buka `db.py` dan ganti `sakura_p00` pada baris `"user"` dengan ID-mu. Folder `koperasi-sekolah` (tanpa ID) adalah contoh asli: **jangan diubah**. Kerjakan hanya di folder yang ada ID-mu.

Cek bahwa semuanya tersambung:

```text
uv run cek.py
```

Awalnya semua contoh gagal. Itu normal, karena `koperasi.py` masih kosong. `cek.py` mengembalikan data koperasi ke data awal setiap kali dijalankan.

## Apa yang dibuat

Program yang membaca perintah satu baris demi satu baris dari input **tanpa mencetak prompt apa pun**, dan berhenti saat input habis. Dijalankan dengan `uv run main.py`.

| Perintah | Yang terjadi |
| --- | --- |
| `isi NAMA NOMINAL` | Menambah saldo siswa. Tidak mencetak apa pun kalau berhasil. |
| `saldo NAMA` | Mencetak `Andi saldo : 30000`. |
| `beli NAMA BARANG JUMLAH` | Siswa membeli barang. Tidak mencetak apa pun kalau berhasil. |
| `laporan` | Mencetak penjualan tiap barang. |
| `stok` | **Bonus.** Mencetak stok tiap barang. |
| `batal NOMOR` | **Bonus.** Membatalkan satu pembelian. Tidak mencetak apa pun kalau berhasil. |

Nama siswa dan nama barang ditulis apa adanya. **Huruf besar dan kecil dibedakan**: `andi` bukan `Andi`. Nama barang tidak memakai spasi (contoh: `Buku_Tulis`). Baris kosong dan perintah yang tidak dikenal diabaikan.

## Aturan `beli`

Pengecekan dilakukan **berurutan**. Berhenti di kegagalan pertama, cetak satu pesan, dan tidak ada data yang berubah.

| Urutan | Kejadian | Pesan |
| --- | --- | --- |
| 1 | Siswa tidak ada | `Siswa tidak ditemukan` |
| 2 | Barang tidak ada | `Barang tidak ditemukan` |
| 3 | Jumlah bukan bilangan bulat 1 atau lebih (`0`, `-1`, `abc`, `1.5`) | `Jumlah tidak valid` |
| 4 | Jumlah barang itu yang sudah dibeli siswa ini, ditambah jumlah baru, melebihi batas | `Melebihi batas pembelian` |
| 5 | Stok kurang dari jumlah | `Stok tidak cukup` |
| 6 | Saldo kurang dari total bayar | `Saldo tidak cukup` |

Soal batas di urutan 4: yang dihitung hanya pembelian yang **tidak dibatalkan**.

Cara menghitung total bayar:

- Subtotal = harga × jumlah.
- Kalau subtotal **mencapai** batas diskon atau lebih, total bayar dipotong sebesar persen diskon.
- Kalau saldo sama persis dengan total bayar, pembelian **berhasil**.
- Semua angka ditulis sebagai bilangan bulat, tanpa koma dan tanpa desimal (`10800`, bukan `10800.0`).

Kalau lolos, saldo berkurang sebesar total bayar, stok berkurang sebesar jumlah, dan satu pembelian dicatat. Nomor pembelian dimulai dari 1 dan hanya bertambah untuk pembelian yang berhasil.

## Aturan `isi`

Pengecekan berurutan: siswa tidak ada (`Siswa tidak ditemukan`), lalu nominal bukan bilangan bulat 1 atau lebih (`Nominal tidak valid`).

## Aturan `laporan`

- Satu baris per barang: `Pensil 3 buah pendapatan : 6000`.
- Urut dari pendapatan terbesar. Kalau pendapatan sama, urut nama barang dari A sampai Z.
- Barang yang belum terjual tetap dicetak, dengan angka 0.
- Pembelian yang dibatalkan tidak dihitung.
- Baris terakhir: `TOTAL 3 buah pendapatan : 6000`.

## Aturan bonus

- `stok`: satu baris per barang urut nomor barang (`id`), bentuknya `Buku_Tulis stok : 20`.
- `batal NOMOR`, pengecekan berurutan:
  1. Nomor bukan bilangan bulat 1 atau lebih, atau tidak ada: `Pembelian tidak ditemukan`.
  2. Pembelian itu sudah dibatalkan: `Pembelian sudah dibatalkan`.

  Kalau lolos: saldo siswa bertambah sebesar **total yang dulu dibayar**, dan stok barang bertambah sebesar jumlah yang dulu dibeli.

## File yang kamu kerjakan

| File | Keadaan | Tugasmu |
| --- | --- | --- |
| `koperasi.py` | kerangka | Isi semua fungsi yang bertanda `TODO`. |
| `main.py` | sudah jadi | Jangan diubah. |
| `aturan.py` | angka aturan ada | Jangan diubah. Angka aturan hanya boleh ada di file ini. |
| `db.py` | sudah jadi | Hanya ganti ID-mu. |
| `db/schema.sql`, `db/seed.sql` | sudah jadi | Jangan diubah. |

Waktu penilaian, `main.py`, `aturan.py`, `db.py`, dan folder `db` diganti dengan versi asli. Hanya `koperasi.py` (dan file tambahan buatanmu) yang dipakai.

## Memeriksa pekerjaanmu

```text
uv run cek.py
```

`cek.py` menjalankan 6 contoh di folder `contoh/`. Penilaian memakai **jauh lebih banyak skenario**, jadi buat skenariomu sendiri dan pikirkan kasus yang belum dicontohkan.

## Mengumpulkan

**Ketik di terminal** (ganti `p00` dengan ID-mu):

```text
cd ~/seti-isd-materi
```

```text
git add minggu-03-database/tugas-akhir/sesi-2-koperasi/koperasi-sekolah-p00
```

```text
git commit -m "Sesi 2: koperasi sekolah"
```

```text
git pull --rebase
```

```text
git push
```

Boleh commit dan push berkali-kali setiap ada kemajuan. Yang dihitung untuk peringkat adalah waktu commit **terakhir**.
