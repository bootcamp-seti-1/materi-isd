# Database 1: Pasang MySQL di Komputermu

## Cerita

Kamu baru masuk PT Sakura Soft. Hari ini Mas Bayu (tim lead) bilang:

> "Aplikasi kita selama ini menyimpan data di file. Mulai minggu ini kita pindah ke database. Pasang MySQL di laptopmu dulu, kita pakai itu untuk semua proyek ke depan."

Tugasmu hari ini: MySQL jalan di Ubuntu (WSL) milikmu, dan kamu bisa masuk ke dalamnya lewat terminal.

Kita **tidak** memakai phpMyAdmin. Semua lewat terminal, seperti yang dilakukan di server sungguhan.

## Yang harus sudah ada

- Ubuntu 24.04 di WSL sudah jalan (dari minggu 1).
- Terminal Ubuntu sudah kamu buka.
- Koneksi internet.

## Langkah 1: Pasang MySQL

Ketik satu per satu di terminal Ubuntu. Setelah itu kamu akan diminta password Ubuntu-mu.

```bash
sudo apt update
```

```bash
sudo apt install mysql-server -y
```

Cek apakah terpasang:

```bash
mysql --version
```

Hasil yang benar: muncul tulisan versi, mirip `mysql  Ver 8.0.xx ... for Linux`.

## Langkah 2: Nyalakan MySQL

```bash
sudo service mysql start
```

Cek statusnya:

```bash
sudo service mysql status
```

Hasil yang benar: ada tulisan `Active: active (running)` atau `mysql is running`.

Catatan: setiap kali Ubuntu/WSL kamu dimatikan dan dibuka lagi, MySQL mati. Jalankan lagi `sudo service mysql start` sebelum bekerja.

## Langkah 3: Masuk pertama kali

Pasang awal MySQL belum punya akun biasa. Masuk dulu sebagai admin:

```bash
sudo mysql
```

Prompt terminalmu akan berubah menjadi `mysql>`. Artinya kamu sudah berada di dalam MySQL. Semua perintah di bagian ini diketik di prompt itu dan **diakhiri titik koma `;`**.

Coba perintah pertama:

```sql
SELECT VERSION();
```

Hasil yang benar: tabel kecil berisi nomor versi.

## Langkah 4: Buat akun dan database milikmu

Masih di prompt `mysql>`, ketik satu per satu.
Ganti `p00` dengan ID pesertamu (huruf kecil), contoh `p07`.

```sql
CREATE DATABASE sakura_db;
```

```sql
CREATE USER 'sakura_p00'@'localhost' IDENTIFIED BY 'sakura123';
```

```sql
GRANT ALL PRIVILEGES ON sakura_db.* TO 'sakura_p00'@'localhost';
```

```sql
FLUSH PRIVILEGES;
```

Cek databasenya sudah ada:

```sql
SHOW DATABASES;
```

Hasil yang benar: ada `sakura_db` di daftar.

Keluar dari MySQL:

```sql
EXIT;
```

Password `sakura123` hanya untuk latihan di laptop sendiri. Jangan pakai password ini untuk hal lain.

## Langkah 5: Masuk dengan akunmu sendiri

Sekarang kamu masuk sebagai pengguna biasa, bukan admin:

```bash
mysql -u sakura_p00 -p sakura_db
```

Saat diminta password, ketik `sakura123` (layar tidak menampilkan apa-apa saat mengetik, itu normal), lalu Enter.

Hasil yang benar: prompt `mysql>` muncul.

Coba:

```sql
SELECT DATABASE();
```

Hasil yang benar: tertulis `sakura_db`.

```sql
SELECT NOW();
```

Hasil yang benar: muncul tanggal dan jam sekarang.

Keluar:

```sql
EXIT;
```

## Selesai kalau

- [ ] `mysql --version` menampilkan versi
- [ ] `sudo service mysql status` menunjukkan running
- [ ] Kamu bisa masuk dengan `mysql -u sakura_p00 -p sakura_db`
- [ ] `SELECT DATABASE();` menampilkan `sakura_db`

Kirim ke Mas Bayu (grup kelas): screenshot terminal yang menunjukkan hasil `SELECT DATABASE();` dan `SELECT NOW();`.

## Kalau macet

| Pesan error | Penyebab | Yang dilakukan |
|---|---|---|
| `ERROR 2002 Can't connect to local MySQL server through socket` | MySQL belum menyala | Jalankan `sudo service mysql start`, ulangi |
| `ERROR 1045 Access denied for user` | Salah nama user atau password | Cek `p00` sudah diganti ID-mu dan password-nya `sakura123` |
| `Unable to locate package mysql-server` | Daftar paket belum diperbarui | Jalankan `sudo apt update`, ulangi langkah 1 |
| `ERROR 1396 Operation CREATE USER failed` | User dengan nama itu sudah pernah dibuat | Lanjut ke `GRANT`, atau tanya fasilitator |
| Prompt `->` muncul terus setelah Enter | Lupa titik koma `;` | Ketik `;` lalu Enter |
| `sudo: mysql: command not found` | MySQL belum terpasang | Ulangi langkah 1 |

Masih macet setelah mencoba sendiri dan bertanya ke AI atau mencari di internet? Panggil fasilitator.

## Tantangan (kalau sudah selesai lebih cepat)

Tanpa melihat materi: keluar dari MySQL, matikan dengan `sudo service mysql stop`, nyalakan lagi, lalu masuk ke `sakura_db` dengan akunmu. Berapa perintah yang kamu butuhkan?

## Opsional: alat bantu tampilan

Kalau nanti ingin melihat tabel dengan tampilan grafis, kamu boleh memakai DBeaver atau ekstensi database di VS Code. Tidak wajib, dan tidak dibahas hari ini. Belajar lewat terminal dulu.