# Hari 3 (Kamis) — Hands-on: sistem perpustakaan SD Harapan

Ikuti langkahnya berurutan, ketik persis, dan cocokkan hasilmu di setiap titik cek. Penjelasan disampaikan trainer sambil mengetik.

Hari ini kamu membuat satu proyek baru dari awal: schema, data, query, dan aplikasi menu, dengan pola yang sama seperti Selasa dan Rabu. Lembar ini memandumu sampai jadi. Setelah selesai, trainer menanyaimu satu per satu: kamu diminta menjelaskan kode dan query yang kamu buat sendiri (lihat bagian "Cara dinilai" di bawah).

## Tujuan hari ini

Pagi ini Mas Bayu masuk ke ruangan dengan wajah cerah:

> "Tim, ada klien baru: perpustakaan SD Harapan. Selama ini guru perpustakaannya mencatat peminjaman buku di buku tulis. Sering ada buku yang tidak jelas ada di mana, dan anak yang belum mengembalikan buku tidak ketahuan. Besok mereka mau lihat demonya. Mereka butuh sistem sederhana: bisa melihat buku dan stok yang tersedia, mencatat peminjaman, mencatat pengembalian, dan melihat siapa yang sedang meminjam apa."

### Hasil akhir yang dikejar hari ini

Isi folder `perpus` di dalam folder kerjamu (ID-mu menggantikan `p00`):

```text
sakura-tasks-p00/
  perpus/
    db/
      schema.sql      tiga tabel: books, members, loans
      seed.sql        data awal
      queries.sql     jawaban lima pertanyaan guru perpustakaan
    db.py             file penghubung ke MySQL (disalin dari Rabu)
    main.py           aplikasi menu
```

Program dijalankan dari folder `perpus`:

```text
uv run main.py
```

Lalu muncul menu:

```text
=== Perpustakaan SD Harapan ===
1. Lihat buku dan sisa stok
2. Pinjam buku
3. Kembalikan buku
4. Lihat buku yang sedang dipinjam
5. Lihat anggota dan jumlah peminjamannya
0. Keluar
```

## Persiapan sebelum mulai

- [ ] Laptop terhubung internet dan baterai aman untuk 2 jam
- [ ] Hari 2 sudah selesai: folder `sakura-tasks-p00` berisi `db.py`, `pyproject.toml`, dan `main.py`, dan `uv run tes_koneksi.py` pernah berhasil (kalau belum, buka Jalur kejar di bagian bawah)
- [ ] VS Code dan `uv` sudah terpasang
- [ ] Aku tahu ID pesertaku, ditulis huruf kecil (contoh: `p01`)

## Peta Hari 3 (115 menit)

| Bagian | Isi | Menit | Hasilnya |
| --- | --- | --- | --- |
| A | Persiapan | 10 | Folder `perpus` siap, sambungan ke MySQL jalan |
| B | Schema | 15 | Tabel `books`, `members`, `loans` ada |
| C | Data awal | 5 | 5 buku, 5 anggota, 6 peminjaman |
| D | Query | 25 | Lima pertanyaan guru terjawab di `queries.sql` |
| E | Aplikasi | 50 | Menu 1 sampai 5 jalan |
| F | Simpan ke Git dan GitHub | 10 | Pekerjaan ter-push |

## Aturan main

1. Ikuti bagian dari A sampai F, berurutan.
2. Ketik hanya isi kotak berlabel **Ketik** atau **Isi file**. Sisanya dibaca saja.
3. Setiap bagian ditutup **Titik cek**. Cocok? Lanjut.
4. Tertinggal? Pakai **Jalur kejar** di bagian bawah, tidak perlu menunggu siapa pun.
5. Stuck? Tulis di grup: ID, bagian, dan tempel pesan error. Contoh: "P08 stuck di E2".
6. Boleh bertanya ke AI atau mencari di internet. Tapi kamu harus bisa menjelaskan sendiri apa yang kamu ketik.

## Cara membaca lembar ini

| Label | Artinya |
| --- | --- |
| **Folder** | Tempat kamu harus berada saat mengetik |
| **File** | Nama file beserta lokasinya. "Baru" berarti kamu yang membuatnya |
| **Isi file** | Teks yang ditempel ke dalam file di VS Code, lalu disimpan dengan `Ctrl+S` |
| **Ketik di terminal** | Perintah yang diketik di terminal, yaitu baris yang berakhir dengan `$` |
| **Ketik di `mysql>`** | Perintah SQL yang diketik setelah masuk ke MySQL, yaitu baris yang diawali `mysql>` |
| **Yang harus muncul di layar** | Hanya dibaca. Jangan diketik |
| **Titik cek** | Cocokkan hasilmu sebelum lanjut |

Ingat dua tempat mengetik yang berbeda: **terminal** (`nama@LAPTOP:~/...$`) dan **di dalam MySQL** (`mysql>`). Password MySQL adalah `sakura123`, dan hurufnya tidak tampil saat diketik.

### Kamus mini

Penjelasannya akan disampaikan trainer sambil mengetik. Tabel ini untuk dibuka kalau kamu ketemu kata yang belum kamu pahami.

| Kata | Artinya | Contoh |
| --- | --- | --- |
| Stok | Jumlah eksemplar buku yang dimiliki perpustakaan | `stock` di tabel `books` |
| Sisa stok | Stok dikurangi jumlah yang sedang dipinjam dan belum kembali | `stock - COUNT(l.id)` |
| Tabel penghubung | Tabel yang menyambungkan dua tabel lain, karena hubungannya banyak-ke-banyak | `loans` menyambungkan `books` dan `members` |
| `date.today()` | Tanggal hari ini di Python | `2026-11-19` |
| `timedelta` | Selisih waktu di Python, bisa ditambahkan ke tanggal | `timedelta(days=7)` |
| `.isdigit()` | Memeriksa apakah teks isinya angka semua | `"12".isdigit()` bernilai benar |

### Kalau kamu tertinggal

Buka **Titik cek** terakhir yang berhasil kamu lewati, cocokkan hasilmu, lalu lanjut. Kalau sudah lebih dari satu bagian tertinggal, pakai **Jalur kejar** di bagian bawah, termasuk `main.py` lengkap.

---

## Bagian A — Persiapan (10 menit)

### A1 — Buka terminal dan nyalakan MySQL

Buka aplikasi **Ubuntu** dari menu Windows.

**Ketik di terminal:**

```text
sudo service mysql start
```

### A2 — Masuk ke folder kerjamu

**Ketik di terminal** (ganti `p00` dengan ID-mu):

```text
cd ~/seti-isd-materi/minggu-03-database/sakura-tasks-p00
```

### A3 — Buat folder perpus dan salin db.py

Tugas hari ini disimpan di subfolder `perpus`, di dalam folder kerjamu. Database yang dipakai tetap `sakura_db` dengan akunmu yang sama. Tabel-tabel baru tidak akan bertabrakan dengan `projects` dan `tasks`.

**Folder:** `sakura-tasks-p00`

**Ketik di terminal:**

```text
mkdir -p perpus/db
```

```text
cp db.py perpus/
```

Perintah kedua menyalin file penghubung dari Rabu ke folder `perpus`. Kalau muncul `No such file or directory`, `db.py` tidak ada: buka Jalur kejar bagian "Kalau Hari 2 belum selesai".

### A4 — Buka VS Code dan masuk ke perpus

**Folder:** `sakura-tasks-p00`

**Ketik di terminal:**

```text
code .
```

**Yang harus muncul di layar:** VS Code terbuka, tertulis **WSL: Ubuntu** di pojok kiri bawah, dan panel kiri menampilkan folder `perpus`. Buka terminal di dalam VS Code dengan `Ctrl` dan tombol backtick (karakter di kiri angka 1). Mulai sekarang semua perintah diketik di terminal VS Code itu.

**Ketik di terminal:**

```text
cd perpus
```

```text
pwd
```

**Yang harus muncul di layar** (nama di komputermu berbeda):

```text
/home/nama/seti-isd-materi/minggu-03-database/sakura-tasks-p00/perpus
```

Kalau kamu membuka terminal baru, masuk lagi ke folder ini dengan:

```text
cd ~/seti-isd-materi/minggu-03-database/sakura-tasks-p00/perpus
```

Tidak perlu `uv init` lagi. Folder `perpus` memakai proyek `uv` dan pustaka dari folder `sakura-tasks-p00`, satu tingkat di atasnya.

### A5 — Tes sambungan dari folder perpus

**Folder:** `perpus`

**Ketik di terminal:**

```text
uv run python -c "from db import fetch_all; print(fetch_all('SELECT 1 AS x'))"
```

**Yang harus muncul di layar:**

```text
[{'x': 1}]
```

### Titik cek A

- [ ] `pwd` berakhir di `/sakura-tasks-p00/perpus`
- [ ] `ls` menampilkan `db` dan `db.py`
- [ ] Tes sambungan menampilkan `[{'x': 1}]`

---

## Bagian B — Schema (15 menit)

Ada tiga tabel: `books` (buku), `members` (anggota perpustakaan, yaitu siswa), dan `loans` (catatan peminjaman). Satu buku bisa dipinjam berkali-kali, dan satu anggota bisa meminjam banyak buku. Tabel `loans` yang menghubungkan keduanya, jadi `loans` punya dua foreign key.

### B1 — Buat file schema.sql

**Folder:** `perpus`

**File:** `db/schema.sql` (baru)

Di panel kiri VS Code, klik kanan folder `db` **yang ada di dalam folder `perpus`**, pilih **New File**, ketik `schema.sql`, lalu Enter.

**Isi file** (tempel, lalu simpan dengan `Ctrl+S`):

```sql
DROP TABLE IF EXISTS loans;
DROP TABLE IF EXISTS members;
DROP TABLE IF EXISTS books;

CREATE TABLE books (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(150) NOT NULL,
  author VARCHAR(100) NOT NULL,
  stock INT NOT NULL DEFAULT 1
);

CREATE TABLE members (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  class_name VARCHAR(20) NOT NULL
);

CREATE TABLE loans (
  id INT AUTO_INCREMENT PRIMARY KEY,
  book_id INT NOT NULL,
  member_id INT NOT NULL,
  borrowed_at DATE NOT NULL,
  due_date DATE NOT NULL,
  returned_at DATE NULL,
  FOREIGN KEY (book_id) REFERENCES books(id),
  FOREIGN KEY (member_id) REFERENCES members(id)
);
```

Hal yang dibahas trainer sambil menunjuk file ini:

- Urutan `DROP TABLE`: `loans` dihapus lebih dulu karena memegang foreign key ke dua tabel lain. Urutan `CREATE TABLE` kebalikannya.
- `returned_at` boleh kosong (`NULL`). Kosong artinya buku belum dikembalikan.
- `stock` bernilai bawaan 1.

### B2 — Jalankan schema.sql

**Folder:** `perpus`

**Ketik di terminal** (ganti `p00` dengan ID-mu):

```text
mysql -u sakura_p00 -p sakura_db < db/schema.sql
```

Saat `Enter password:` muncul, ketik `sakura123` lalu Enter.

**Yang harus muncul di layar:** tidak ada tulisan apa-apa (artinya berhasil).

### B3 — Periksa hasilnya

**Ketik di terminal:**

```text
mysql -u sakura_p00 -p sakura_db
```

**Ketik di `mysql>`:**

```text
SHOW TABLES;
```

**Yang harus muncul di layar:** tabel `books`, `loans`, `members`, dan juga `projects` dan `tasks` dari hari sebelumnya.

**Ketik di `mysql>`:**

```text
DESCRIBE loans;
```

**Yang harus muncul di layar:** 6 baris. Kolom `Field` berisi: `id`, `book_id`, `member_id`, `borrowed_at`, `due_date`, `returned_at`.

**Ketik di `mysql>`:**

```text
EXIT;
```

### Titik cek B

- [ ] `books`, `members`, dan `loans` ada di `SHOW TABLES;`
- [ ] `DESCRIBE loans;` menampilkan 6 baris

---

## Bagian C — Data awal (5 menit)

### C1 — Buat file seed.sql

**Folder:** `perpus`

**File:** `db/seed.sql` (baru, di folder `db` yang ada di dalam `perpus`)

**Isi file** (tempel, lalu simpan dengan `Ctrl+S`):

```sql
INSERT INTO books (title, author, stock) VALUES
  ('Belajar Matematika Asyik', 'Bu Ratna', 3),
  ('Kisah Si Kancil', 'Pak Anwar', 2),
  ('Ensiklopedia Hewan', 'Tim Redaksi', 1),
  ('Dasar-Dasar Komputer', 'Pak Dimas', 2),
  ('Cerita Rakyat Nusantara', 'Bu Sari', 1);

INSERT INTO members (name, class_name) VALUES
  ('Andi', '5A'),
  ('Bunga', '5A'),
  ('Citra', '6B'),
  ('Dika', '4C'),
  ('Eka', '6B');

INSERT INTO loans (book_id, member_id, borrowed_at, due_date, returned_at) VALUES
  (1, 1, '2026-11-02', '2026-11-09', '2026-11-08'),
  (2, 1, '2026-11-10', '2026-11-17', NULL),
  (3, 2, '2026-11-03', '2026-11-10', '2026-11-12'),
  (1, 3, '2026-11-05', '2026-11-12', NULL),
  (4, 3, '2026-11-11', '2026-11-18', NULL),
  (2, 4, '2026-11-09', '2026-11-16', '2026-11-15');
```

### C2 — Jalankan seed.sql

**Ketik di terminal:**

```text
mysql -u sakura_p00 -p sakura_db < db/seed.sql
```

**Yang harus muncul di layar:** tidak ada tulisan apa-apa (artinya berhasil).

### C3 — Periksa isinya

**Ketik di terminal:**

```text
mysql -u sakura_p00 -p sakura_db -e "SELECT COUNT(*) AS jumlah FROM loans"
```

**Yang harus muncul di layar:**

```text
jumlah
6
```

### Titik cek C

- [ ] Tabel `loans` berisi 6 baris
- [ ] Kalau `seed.sql` error, biasanya `schema.sql` salah ketik. Perbaiki `schema.sql`, jalankan ulang (B2), lalu jalankan `seed.sql` lagi

---

## Bagian D — Query: lima pertanyaan guru perpustakaan (25 menit)

Guru perpustakaan mengajukan lima pertanyaan. Jawabannya kita tulis sebagai query di satu file, lalu dijalankan sekaligus.

### D1 — Buat file queries.sql

**Folder:** `perpus`

**File:** `db/queries.sql` (baru, di folder `db` yang ada di dalam `perpus`)

**Isi file** (tempel, lalu simpan dengan `Ctrl+S`):

```sql
-- Soal 1: buku yang sedang dipinjam (belum dikembalikan)
SELECT b.title, m.name, m.class_name, l.due_date
FROM loans l
JOIN books b ON b.id = l.book_id
JOIN members m ON m.id = l.member_id
WHERE l.returned_at IS NULL
ORDER BY l.due_date;

-- Soal 2: anggota yang belum pernah meminjam buku
SELECT m.name
FROM members m
LEFT JOIN loans l ON l.member_id = m.id
WHERE l.id IS NULL;

-- Soal 3: berapa kali tiap buku dipinjam
SELECT b.title, COUNT(l.id) AS jumlah_pinjam
FROM books b
LEFT JOIN loans l ON l.book_id = b.id
GROUP BY b.id, b.title
ORDER BY b.id;

-- Soal 4: sisa eksemplar tiap buku yang bisa dipinjam
SELECT b.title, b.stock - COUNT(l.id) AS sisa
FROM books b
LEFT JOIN loans l ON l.book_id = b.id AND l.returned_at IS NULL
GROUP BY b.id, b.title, b.stock
ORDER BY b.id;

-- Soal 5: anggota yang mengembalikan buku terlambat
SELECT m.name, b.title, l.due_date, l.returned_at
FROM loans l
JOIN books b ON b.id = l.book_id
JOIN members m ON m.id = l.member_id
WHERE l.returned_at > l.due_date;
```

### D2 — Jalankan semua query

**Ketik di terminal:**

```text
mysql -t -u sakura_p00 -p sakura_db < db/queries.sql
```

Tulisan `-t` membuat hasilnya tampil sebagai tabel. Lima tabel hasil muncul berurutan.

### D3 — Cocokkan hasilnya

**Soal 1.** Guru: "Buku apa saja yang sekarang sedang dipinjam? Tampilkan judul buku, nama peminjam, kelasnya, dan batas tanggal kembali." Hasilnya 3 baris:

| title | name | class_name | due_date |
| --- | --- | --- | --- |
| Belajar Matematika Asyik | Citra | 6B | 2026-11-12 |
| Kisah Si Kancil | Andi | 5A | 2026-11-17 |
| Dasar-Dasar Komputer | Citra | 6B | 2026-11-18 |

**Soal 2.** Guru: "Ada anak yang belum pernah meminjam buku sama sekali?" Hasilnya 1 baris: `Eka`.

**Soal 3.** Guru: "Tiap buku sudah dipinjam berapa kali?" Hasilnya:

| title | jumlah_pinjam |
| --- | --- |
| Belajar Matematika Asyik | 2 |
| Kisah Si Kancil | 2 |
| Ensiklopedia Hewan | 1 |
| Dasar-Dasar Komputer | 1 |
| Cerita Rakyat Nusantara | 0 |

**Soal 4.** Guru: "Tiap buku sekarang tersisa berapa eksemplar yang bisa dipinjam?" Hasilnya:

| title | sisa |
| --- | --- |
| Belajar Matematika Asyik | 2 |
| Kisah Si Kancil | 1 |
| Ensiklopedia Hewan | 1 |
| Dasar-Dasar Komputer | 1 |
| Cerita Rakyat Nusantara | 1 |

**Soal 5.** Guru: "Siapa yang mengembalikan buku terlambat?" Hasilnya 1 baris: `Bunga`, `Ensiklopedia Hewan`, `2026-11-10`, `2026-11-12`.

### D4 — Hal yang dibahas trainer

Dibaca saja, supaya kamu siap kalau ditanya:

- **Soal 2, 3, dan 4 memakai `LEFT JOIN`.** Dengan `JOIN` biasa, anggota atau buku yang belum punya peminjaman hilang dari hasil.
- **Soal 4: syarat `l.returned_at IS NULL` ada di `ON`, bukan di `WHERE`.** Kalau ditaruh di `WHERE`, buku yang tidak sedang dipinjam (Ensiklopedia Hewan, Cerita Rakyat Nusantara) ikut hilang dari hasil.
- **Soal 3 memakai `COUNT(l.id)`, bukan `COUNT(*)`.** `COUNT(*)` menghitung satu baris untuk buku yang belum pernah dipinjam, jadi angkanya salah.
- **Soal 5 membandingkan dua kolom tanggal.** Peminjaman yang belum dikembalikan (`returned_at` kosong) tidak ikut, karena nilai kosong tidak bisa dibandingkan.

### Titik cek D

- [ ] Lima tabel hasil muncul, tanpa pesan `ERROR`
- [ ] Soal 1 menghasilkan 3 baris, Soal 2 menghasilkan `Eka`, Soal 5 menghasilkan `Bunga`
- [ ] Soal 3 dan Soal 4 sama persis dengan tabel di atas
- [ ] Kamu bisa menjelaskan ke teman: kenapa Soal 4 memakai `LEFT JOIN`

---

## Bagian E — Aplikasi (50 menit)

Aplikasi ini bekerja seperti Sakura Tasks kemarin. Boleh membuka lagi `main.py` di folder `sakura-tasks-p00` (satu tingkat di atas folder `perpus`) sebagai contoh polanya.

### E1 — Kerangka aplikasi dan menu yang hanya membaca data (menu 1, 4, 5)

**Folder:** `perpus`

**File:** `main.py` (baru, langsung di folder `perpus`)

Di panel kiri VS Code, klik kanan folder `perpus`, pilih **New File**, ketik `main.py`, lalu Enter.

**Isi file** (tempel, lalu simpan dengan `Ctrl+S`). Menu 1, 4, dan 5 sudah jadi. Menu 2 dan 3 masih berisi tulisan "Fitur ini belum dibuat", dan itu diisi di E3 dan E4:

```python
from datetime import date, timedelta

import mysql.connector

from db import fetch_all, execute

LAMA_PINJAM = 7

SQL_SISA_BUKU = """
    SELECT b.id, b.title, b.author, b.stock - COUNT(l.id) AS sisa
    FROM books b
    LEFT JOIN loans l ON l.book_id = b.id AND l.returned_at IS NULL
    GROUP BY b.id, b.title, b.author, b.stock
    ORDER BY b.id
"""


def minta_angka(pertanyaan):
    teks = input(pertanyaan).strip()
    if not teks.isdigit():
        print("Isi dengan angka.")
        return None
    return int(teks)


def lihat_buku():
    print("\n=== Daftar Buku ===")
    for b in fetch_all(SQL_SISA_BUKU):
        print(f"[{b['id']}] {b['title']} - {b['author']} | sisa: {b['sisa']}")


def lihat_dipinjam():
    sql = """
        SELECT l.id, b.title, m.name, m.class_name, l.due_date
        FROM loans l
        JOIN books b ON b.id = l.book_id
        JOIN members m ON m.id = l.member_id
        WHERE l.returned_at IS NULL
        ORDER BY l.due_date
    """
    rows = fetch_all(sql)
    print("\n=== Buku yang Sedang Dipinjam ===")
    if not rows:
        print("Tidak ada buku yang sedang dipinjam.")
        return rows
    hari_ini = date.today()
    for r in rows:
        penanda = " TERLAMBAT" if r["due_date"] < hari_ini else ""
        print(
            f"[{r['id']}] {r['title']} | {r['name']} ({r['class_name']}) | "
            f"batas: {r['due_date']}{penanda}"
        )
    return rows


def lihat_anggota():
    sql = """
        SELECT m.id, m.name, m.class_name, COUNT(l.id) AS jumlah
        FROM members m
        LEFT JOIN loans l ON l.member_id = m.id
        GROUP BY m.id, m.name, m.class_name
        ORDER BY m.id
    """
    print("\n=== Daftar Anggota ===")
    for r in fetch_all(sql):
        print(f"[{r['id']}] {r['name']} ({r['class_name']}) | pernah meminjam: {r['jumlah']} kali")


def pinjam_buku():
    print("Fitur ini belum dibuat (menu 2)")


def kembalikan_buku():
    print("Fitur ini belum dibuat (menu 3)")


MENU = """
=== Perpustakaan SD Harapan ===
1. Lihat buku dan sisa stok
2. Pinjam buku
3. Kembalikan buku
4. Lihat buku yang sedang dipinjam
5. Lihat anggota dan jumlah peminjamannya
0. Keluar
"""

AKSI = {
    "1": lihat_buku,
    "2": pinjam_buku,
    "3": kembalikan_buku,
    "4": lihat_dipinjam,
    "5": lihat_anggota,
}


def main():
    while True:
        print(MENU)
        pilihan = input("Pilih menu: ").strip()
        if pilihan == "0":
            print("Sampai jumpa!")
            break
        aksi = AKSI.get(pilihan)
        if aksi is None:
            print("Menu tidak dikenal.")
            continue
        try:
            aksi()
        except mysql.connector.Error as e:
            print(f"Ada masalah di database: {e}")


if __name__ == "__main__":
    main()
```

### E2 — Jalankan dan uji menu 1, 4, 5

**Folder:** `perpus`

**Ketik di terminal:**

```text
uv run main.py
```

Ketik `1` di `Pilih menu:`. **Yang harus muncul di layar:**

```text
=== Daftar Buku ===
[1] Belajar Matematika Asyik - Bu Ratna | sisa: 2
[2] Kisah Si Kancil - Pak Anwar | sisa: 1
[3] Ensiklopedia Hewan - Tim Redaksi | sisa: 1
[4] Dasar-Dasar Komputer - Pak Dimas | sisa: 1
[5] Cerita Rakyat Nusantara - Bu Sari | sisa: 1
```

Angka `sisa` sama dengan hasil Soal 4 di Bagian D. Query-nya sama, hanya dipanggil dari Python.

Ketik `4`. **Yang harus muncul di layar:** 3 buku yang belum kembali. Batas kembali ketiganya (12, 17, dan 18 November 2026) sudah lewat pada hari Kamis, 19 November 2026, jadi ketiganya diberi tanda `TERLAMBAT`. Kalau kamu mengerjakan di tanggal lain, tanda `TERLAMBAT` hanya muncul di baris yang batasnya sudah lewat dari tanggal hari itu.

Ketik `5`. **Yang harus muncul di layar:** 5 anggota. Jumlah pinjam: Andi 2, Bunga 1, Citra 2, Dika 1, Eka 0. Eka tetap muncul dengan angka 0.

Ketik `0` untuk keluar.

### E3 — Menu 2: pinjam buku

**File:** `main.py`

Cari dua baris ini dan **hapus keduanya**:

```python
def pinjam_buku():
    print("Fitur ini belum dibuat (menu 2)")
```

**Isi file:** tempel ini di tempat yang sama:

```python
def pinjam_buku():
    lihat_buku()
    anggota_id = minta_angka("Nomor anggota: ")
    if anggota_id is None:
        return
    buku_id = minta_angka("Nomor buku: ")
    if buku_id is None:
        return
    anggota = fetch_all("SELECT name FROM members WHERE id = %s", (anggota_id,))
    if not anggota:
        print("Nomor anggota tidak ditemukan.")
        return
    buku = [b for b in fetch_all(SQL_SISA_BUKU) if b["id"] == buku_id]
    if not buku:
        print("Nomor buku tidak ditemukan.")
        return
    buku = buku[0]
    if buku["sisa"] <= 0:
        print(f"Maaf, stok '{buku['title']}' sedang habis.")
        return
    hari_ini = date.today()
    batas = hari_ini + timedelta(days=LAMA_PINJAM)
    execute(
        "INSERT INTO loans (book_id, member_id, borrowed_at, due_date) "
        "VALUES (%s, %s, %s, %s)",
        (buku_id, anggota_id, hari_ini, batas),
    )
    print(
        f"Berhasil: {anggota[0]['name']} meminjam '{buku['title']}'. "
        f"Batas kembali: {batas}"
    )
```

Simpan dengan `Ctrl+S`. Hal yang dibahas trainer:

- Tiga penolakan (nomor anggota tidak ada, nomor buku tidak ada, stok 0) terjadi **sebelum** `execute`. Data baru disimpan hanya kalau semuanya lolos.
- `batas` dihitung dari `hari_ini + timedelta(days=LAMA_PINJAM)`, yaitu 7 hari.
- Nilai dari pengguna masuk ke SQL lewat `%s`, bukan f-string.

### E4 — Menu 3: kembalikan buku

**File:** `main.py`

Cari dua baris ini dan **hapus keduanya**:

```python
def kembalikan_buku():
    print("Fitur ini belum dibuat (menu 3)")
```

**Isi file:** tempel ini di tempat yang sama:

```python
def kembalikan_buku():
    rows = lihat_dipinjam()
    if not rows:
        return
    nomor = minta_angka("Nomor peminjaman yang dikembalikan: ")
    if nomor is None:
        return
    sql = """
        SELECT l.due_date, l.returned_at, b.title, m.name
        FROM loans l
        JOIN books b ON b.id = l.book_id
        JOIN members m ON m.id = l.member_id
        WHERE l.id = %s
    """
    hasil = fetch_all(sql, (nomor,))
    if not hasil:
        print("Nomor peminjaman tidak ditemukan.")
        return
    p = hasil[0]
    if p["returned_at"] is not None:
        print("Buku ini sudah dikembalikan sebelumnya.")
        return
    hari_ini = date.today()
    execute("UPDATE loans SET returned_at = %s WHERE id = %s", (hari_ini, nomor))
    print(f"Berhasil: {p['name']} mengembalikan '{p['title']}'.")
    telat = (hari_ini - p["due_date"]).days
    if telat > 0:
        print(f"Peringatan: terlambat {telat} hari.")
```

Simpan dengan `Ctrl+S`. Hal yang dibahas trainer:

- Daftar buku yang sedang dipinjam (menu 4) dipakai ulang, supaya pengguna tahu nomor peminjamannya.
- Pengecekan `returned_at is not None` mencegah satu peminjaman dikembalikan dua kali.
- `execute` memanggil `commit` di dalam `db.py`, jadi perubahan benar-benar tersimpan.

### E5 — Uji menu 2 dan 3

**Folder:** `perpus`

**Ketik di terminal:**

```text
uv run main.py
```

Uji **meminjam buku yang lolos**. Eka belum pernah meminjam, dan buku nomor 3 (Ensiklopedia Hewan) tersisa 1:

| Pertanyaan di layar | Ketik |
| --- | --- |
| `Pilih menu:` | `2` |
| `Nomor anggota:` | `5` |
| `Nomor buku:` | `3` |

**Yang harus muncul di layar:** `Berhasil: Eka meminjam 'Ensiklopedia Hewan'. Batas kembali: ...`, dengan tanggal batas tepat 7 hari dari hari ini.

Uji **stok habis**. Buku nomor 3 sekarang sisa 0:

| Pertanyaan di layar | Ketik |
| --- | --- |
| `Pilih menu:` | `2` |
| `Nomor anggota:` | `4` |
| `Nomor buku:` | `3` |

**Yang harus muncul di layar:** `Maaf, stok 'Ensiklopedia Hewan' sedang habis.`

Uji **nomor yang tidak ada**. Ketik `2`, nomor anggota `99`, nomor buku `1`. **Yang harus muncul:** `Nomor anggota tidak ditemukan.` Ketik `2`, nomor anggota `1`, nomor buku `99`. **Yang harus muncul:** `Nomor buku tidak ditemukan.`

Uji **mengembalikan buku**. Di daftar yang muncul, cari nomor peminjaman (angka di dalam kurung siku) milik `Belajar Matematika Asyik` dan Citra. Nomornya `4`:

| Pertanyaan di layar | Ketik |
| --- | --- |
| `Pilih menu:` | `3` |
| `Nomor peminjaman yang dikembalikan:` | `4` |

**Yang harus muncul di layar:** `Berhasil: Citra mengembalikan 'Belajar Matematika Asyik'.` Batas kembali peminjaman ini 12 November 2026, jadi muncul juga `Peringatan: terlambat ... hari.` Pada hari Kamis, 19 November 2026, angkanya 7 hari.

Uji **mengembalikan buku yang sudah dikembalikan**. Ketik `3`, lalu nomor peminjaman `1`. Peminjaman nomor 1 sudah selesai dari data awal, jadi tidak muncul di daftar, tapi nomornya tetap bisa diketik. **Yang harus muncul:** `Buku ini sudah dikembalikan sebelumnya.`

Ketik `1`: sisa stok `Belajar Matematika Asyik` sekarang 3 dan `Ensiklopedia Hewan` 0. Ketik `0` untuk keluar.

### Titik cek E

- [ ] Menu 1, 4, dan 5 menampilkan hasil seperti di E2
- [ ] Meminjam buku berhasil dan menu 1 menampilkan sisa stok yang berkurang
- [ ] Meminjam buku dengan sisa stok 0 ditolak
- [ ] Nomor anggota atau nomor buku yang tidak ada ditolak
- [ ] Mengembalikan buku berhasil, dan peminjaman yang terlambat menampilkan peringatan
- [ ] Mengembalikan buku yang sudah dikembalikan ditolak
- [ ] Tekan `Ctrl+F` di `main.py`, cari `belum dibuat`: tidak ada hasil

---

## Bagian F — Simpan ke Git dan GitHub (10 menit)

Keluar dari program dengan `0` kalau masih berjalan. Pekerjaanmu disimpan ke repo bersama. Hanya folder milikmu yang disimpan.

**Ketik di terminal:**

```text
cd ~/seti-isd-materi
```

**Ketik di terminal** (ganti `p00` dengan ID-mu):

```text
git add minggu-03-database/sakura-tasks-p00
```

```text
git commit -m "Tugas minggu 3: sistem perpustakaan (schema, query, aplikasi)"
```

```text
git pull --rebase
```

```text
git push
```

Kalian semua menyimpan ke repo yang sama, jadi `git pull --rebase` mengambil pekerjaan teman yang sudah lebih dulu dikirim. Kalau `git push` ditolak dengan tulisan `rejected` atau `fetch first`, ulangi `git pull --rebase`, lalu `git push`.

Buka repo di GitHub lewat browser, lalu pastikan folder `minggu-03-database/sakura-tasks-p00` berisi subfolder `perpus` dengan `main.py`, `db.py`, dan folder `db` (`schema.sql`, `seed.sql`, `queries.sql`).

### Titik cek F

- [ ] `git push` selesai tanpa error
- [ ] Folder `perpus` dengan semua filenya ada di folder milikmu di GitHub

---

## Cara dinilai

Setelah selesai, trainer menanyaimu satu per satu. Kamu diminta menjelaskan query dan kode di folder `perpus` milikmu, misalnya kenapa `loans` punya dua foreign key, kenapa Soal 4 memakai `LEFT JOIN`, dan apa gunanya `commit`. Kalau kamu tidak bisa menjelaskan bagian yang kamu kerjakan sendiri, nilaimu dikurangi.

Nilai tugas dari rubrik 8 kriteria, masing-masing 0 sampai 10 (total 80). Per kriteria: 10 kalau benar penuh, 5 kalau sebagian benar, 0 kalau belum ada. Kompeten kalau nilai akhir (kuis + rubrik) minimal 70.

| No | Kriteria |
| --- | --- |
| 1 | Schema: tiga tabel, nama kolom dan tipe sesuai kebutuhan, primary key benar |
| 2 | Relasi dan aturan: foreign key, `NOT NULL`, `DEFAULT` benar, `returned_at` boleh kosong |
| 3 | `schema.sql` dan `seed.sql` bisa dijalankan berulang tanpa error |
| 4 | Query dengan `JOIN` (Soal 1 dan 5) |
| 5 | Query dengan `LEFT JOIN` dan penghitungan (Soal 2, 3, 4) |
| 6 | Aplikasi: menu yang hanya membaca data (menu 1, 4, 5) |
| 7 | Aplikasi: menu yang mengubah data, lengkap dengan penolakan input yang salah (menu 2 dan 3) |
| 8 | Keamanan dan kerapian: memakai `%s`, `commit`, error ditangani, kode terbaca |

Kuis di Google Form dan soal tambahan dikerjakan terpisah.

## Titik cek akhir Hari 3 dan jika ada masalah

### Target minimal Hari 3

- [ ] `schema.sql`, `seed.sql`, dan `queries.sql` ada di folder `perpus/db` di dalam `sakura-tasks-p00` milikmu
- [ ] `perpus/main.py` jalan dengan `uv run main.py`, dan menu 1 sampai 5 bekerja
- [ ] Kamu pernah mencoba meminjam buku dengan sisa stok 0 dan melihat aplikasi menolaknya
- [ ] Kamu pernah mengembalikan buku yang sudah dikembalikan dan melihat aplikasi menolaknya
- [ ] Kamu bisa menjelaskan ke trainer: kenapa `loans` punya dua foreign key, dan kenapa Soal 4 memakai `LEFT JOIN`
- [ ] Pekerjaanmu sudah di-push dan terlihat di GitHub

### Masalah yang sering muncul

| Pesan error | Penyebab | Yang dilakukan |
| --- | --- | --- |
| `ModuleNotFoundError: No module named 'mysql'` | Pustaka belum dipasang di proyek `sakura-tasks-p00` (mungkin karena Hari 2 terlewat), atau programnya dijalankan dengan `python` biasa | Pindah ke folder `sakura-tasks-p00`, jalankan `uv add mysql-connector-python`, lalu kembali ke `perpus` dan jalankan `uv run main.py` |
| `ModuleNotFoundError: No module named 'db'` | `db.py` belum disalin ke folder `perpus`, atau kamu di folder yang salah | Pindah ke `~/seti-isd-materi/minggu-03-database/sakura-tasks-p00/perpus`, lalu ulangi perintah `cp db.py perpus/` di A3 dari folder `sakura-tasks-p00` |
| `2003 (HY000): Can't connect to MySQL server` | MySQL belum menyala | `sudo service mysql start` |
| `1045 (28000): Access denied` | Salah user atau password di `db.py` | Cek `p00` sudah diganti ID-mu |
| `1215 (HY000): Cannot add foreign key constraint` | Tipe kolom FK tidak sama dengan PK yang ditunjuk, atau tabel yang ditunjuk belum dibuat | Cocokkan `schema.sql` dengan lembar ini, terutama urutan `CREATE TABLE` |
| `3730 ... Cannot drop table ... referenced by a foreign key constraint` | Urutan `DROP TABLE` salah | `loans` harus dihapus lebih dulu, lalu `members`, lalu `books` |
| `1136 (21S01): Column count doesn't match value count` | Jumlah kolom di `seed.sql` tidak cocok dengan tabelmu | Bandingkan `schema.sql` dan `seed.sql` dengan lembar ini |
| `1054 (42S22): Unknown column` | Nama kolom salah ketik | Cek dengan `DESCRIBE nama_tabel;` |
| `IndentationError` atau `SyntaxError` | Salah tempel, atau spasi di awal baris tergeser | Periksa baris yang disebut di pesan error |
| `NameError: name '...' is not defined` | Fungsi terhapus, atau salah ketik nama | Cocokkan dengan `main.py` lengkap di Jalur kejar |
| Perubahan data hilang setelah aplikasi ditutup | Lupa `commit` | Pastikan memakai `execute` dari `db.py` |
| `git push` ditolak (`rejected`, `fetch first`) | Teman sudah lebih dulu mengirim pekerjaan | `git pull --rebase`, lalu `git push` lagi |

Setelah mencoba sendiri dan bertanya ke AI atau mencari di internet masih macet? Tulis di grup.

### Jalur kejar

**Kalau Hari 2 belum selesai (belum ada `db.py` atau `pyproject.toml`).** Kerjakan Bagian C dari lembar Hari 2 (C1 sampai C4: `uv init`, `uv add mysql-connector-python`, `.gitignore`, dan `db.py`), lalu kembali ke Bagian A lembar ini. Bagian `main.py` Sakura Tasks tidak wajib untuk hari ini.

**Kalau tertinggal di Bagian B sampai D.** Salin teks `schema.sql`, `seed.sql`, dan `queries.sql` dari lembar ini ke `perpus/db`, jalankan `schema.sql` lalu `seed.sql` (B2 dan C2), lalu lanjut ke Bagian E.

**Kalau tertinggal di Bagian E.** Ganti seluruh isi `perpus/main.py` dengan versi lengkap berikut (klik `main.py`, `Ctrl+A`, `Delete`, tempel, `Ctrl+S`), lalu lompat ke uji di E5:

```python
from datetime import date, timedelta

import mysql.connector

from db import fetch_all, execute

LAMA_PINJAM = 7

SQL_SISA_BUKU = """
    SELECT b.id, b.title, b.author, b.stock - COUNT(l.id) AS sisa
    FROM books b
    LEFT JOIN loans l ON l.book_id = b.id AND l.returned_at IS NULL
    GROUP BY b.id, b.title, b.author, b.stock
    ORDER BY b.id
"""


def minta_angka(pertanyaan):
    teks = input(pertanyaan).strip()
    if not teks.isdigit():
        print("Isi dengan angka.")
        return None
    return int(teks)


def lihat_buku():
    print("\n=== Daftar Buku ===")
    for b in fetch_all(SQL_SISA_BUKU):
        print(f"[{b['id']}] {b['title']} - {b['author']} | sisa: {b['sisa']}")


def lihat_dipinjam():
    sql = """
        SELECT l.id, b.title, m.name, m.class_name, l.due_date
        FROM loans l
        JOIN books b ON b.id = l.book_id
        JOIN members m ON m.id = l.member_id
        WHERE l.returned_at IS NULL
        ORDER BY l.due_date
    """
    rows = fetch_all(sql)
    print("\n=== Buku yang Sedang Dipinjam ===")
    if not rows:
        print("Tidak ada buku yang sedang dipinjam.")
        return rows
    hari_ini = date.today()
    for r in rows:
        penanda = " TERLAMBAT" if r["due_date"] < hari_ini else ""
        print(
            f"[{r['id']}] {r['title']} | {r['name']} ({r['class_name']}) | "
            f"batas: {r['due_date']}{penanda}"
        )
    return rows


def lihat_anggota():
    sql = """
        SELECT m.id, m.name, m.class_name, COUNT(l.id) AS jumlah
        FROM members m
        LEFT JOIN loans l ON l.member_id = m.id
        GROUP BY m.id, m.name, m.class_name
        ORDER BY m.id
    """
    print("\n=== Daftar Anggota ===")
    for r in fetch_all(sql):
        print(f"[{r['id']}] {r['name']} ({r['class_name']}) | pernah meminjam: {r['jumlah']} kali")


def pinjam_buku():
    lihat_buku()
    anggota_id = minta_angka("Nomor anggota: ")
    if anggota_id is None:
        return
    buku_id = minta_angka("Nomor buku: ")
    if buku_id is None:
        return
    anggota = fetch_all("SELECT name FROM members WHERE id = %s", (anggota_id,))
    if not anggota:
        print("Nomor anggota tidak ditemukan.")
        return
    buku = [b for b in fetch_all(SQL_SISA_BUKU) if b["id"] == buku_id]
    if not buku:
        print("Nomor buku tidak ditemukan.")
        return
    buku = buku[0]
    if buku["sisa"] <= 0:
        print(f"Maaf, stok '{buku['title']}' sedang habis.")
        return
    hari_ini = date.today()
    batas = hari_ini + timedelta(days=LAMA_PINJAM)
    execute(
        "INSERT INTO loans (book_id, member_id, borrowed_at, due_date) "
        "VALUES (%s, %s, %s, %s)",
        (buku_id, anggota_id, hari_ini, batas),
    )
    print(
        f"Berhasil: {anggota[0]['name']} meminjam '{buku['title']}'. "
        f"Batas kembali: {batas}"
    )


def kembalikan_buku():
    rows = lihat_dipinjam()
    if not rows:
        return
    nomor = minta_angka("Nomor peminjaman yang dikembalikan: ")
    if nomor is None:
        return
    sql = """
        SELECT l.due_date, l.returned_at, b.title, m.name
        FROM loans l
        JOIN books b ON b.id = l.book_id
        JOIN members m ON m.id = l.member_id
        WHERE l.id = %s
    """
    hasil = fetch_all(sql, (nomor,))
    if not hasil:
        print("Nomor peminjaman tidak ditemukan.")
        return
    p = hasil[0]
    if p["returned_at"] is not None:
        print("Buku ini sudah dikembalikan sebelumnya.")
        return
    hari_ini = date.today()
    execute("UPDATE loans SET returned_at = %s WHERE id = %s", (hari_ini, nomor))
    print(f"Berhasil: {p['name']} mengembalikan '{p['title']}'.")
    telat = (hari_ini - p["due_date"]).days
    if telat > 0:
        print(f"Peringatan: terlambat {telat} hari.")


MENU = """
=== Perpustakaan SD Harapan ===
1. Lihat buku dan sisa stok
2. Pinjam buku
3. Kembalikan buku
4. Lihat buku yang sedang dipinjam
5. Lihat anggota dan jumlah peminjamannya
0. Keluar
"""

AKSI = {
    "1": lihat_buku,
    "2": pinjam_buku,
    "3": kembalikan_buku,
    "4": lihat_dipinjam,
    "5": lihat_anggota,
}


def main():
    while True:
        print(MENU)
        pilihan = input("Pilih menu: ").strip()
        if pilihan == "0":
            print("Sampai jumpa!")
            break
        aksi = AKSI.get(pilihan)
        if aksi is None:
            print("Menu tidak dikenal.")
            continue
        try:
            aksi()
        except mysql.connector.Error as e:
            print(f"Ada masalah di database: {e}")


if __name__ == "__main__":
    main()
```

**Kalau datamu berantakan dan ingin mengulang dari awal.** Jalankan lagi `schema.sql` (B2), lalu `seed.sql` (C2). Dua file itu mengembalikan tabel perpustakaan ke keadaan awal.
