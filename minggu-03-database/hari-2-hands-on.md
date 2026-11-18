# Hari 2 (Rabu) — Hands-on: JOIN dan aplikasi Sakura Tasks

Ikuti langkahnya berurutan, ketik persis, dan cocokkan hasilmu di setiap titik cek. Penjelasan disampaikan trainer sambil mengetik.

## Tujuan hari ini

Kemarin datamu sudah di database. Pagi ini Mas Bayu (tim lead PT Sakura Soft) datang lagi:

> "Datanya sudah di database, bagus. Tapi waktu saya lihat tabel `tasks`, kolom proyeknya cuma angka: 1, 2, 3. Saya butuh nama proyeknya. Dan satu hal lagi: tim saya bukan orang database. Mereka tidak mau mengetik SQL. Mereka mau aplikasi dengan menu. Hari ini tolong selesaikan dua-duanya."

Dua pekerjaan hari ini:

1. Menggabungkan data dua tabel dengan **JOIN**.
2. Membuat aplikasi menu di terminal (Python) yang menyimpan datanya di MySQL. Aplikasi seperti ini disebut **database-driven application**: tampilan dan logikanya ada di kode, datanya ada di database.

### Hasil akhir yang dikejar hari ini

Isi folder kerjamu (ID-mu menggantikan `p00`):

```text
sakura-tasks-p00/
  db/
    schema.sql      dari Hari 1
    seed.sql        dari Hari 1
    latihan.sql     dari Hari 1
    join.sql        jawaban latihan JOIN hari ini
  db.py             file penghubung ke MySQL
  tes_koneksi.py    tes sambungan
  main.py           aplikasi menu
  pyproject.toml    identitas proyek (dibuat uv)
```

Program dijalankan dari terminal, di folder `sakura-tasks-p00`:

```text
uv run main.py
```

Lalu muncul menu:

```text
=== Sakura Tasks ===
1. Lihat proyek
2. Lihat tugas
3. Tambah tugas
4. Ubah status tugas
5. Hapus tugas
6. Laporan jumlah tugas per proyek
0. Keluar

Pilih menu:
```

## Persiapan sebelum mulai

- [ ] Laptop terhubung internet dan baterai aman untuk 2 jam
- [ ] Hari 1 sudah selesai. Folder `~/seti-isd-materi/minggu-03-database/sakura-tasks-p00/db` berisi `schema.sql` dan `seed.sql` (kalau belum, buka Jalur kejar Hari 1)
- [ ] VS Code, Python 3.12, dan `uv` sudah terpasang (sama seperti minggu lalu)
- [ ] Aku tahu ID pesertaku, ditulis huruf kecil (contoh: `p01`)

## Peta Hari 2 (115 menit)

| Bagian | Isi | Menit | Hasilnya |
| --- | --- | --- | --- |
| A | Persiapan dan reset data | 10 | MySQL menyala, data kembali ke 8 tugas, proyek baru tanpa tugas |
| B | JOIN | 30 | Bisa menggabungkan `tasks` dan `projects`, dan jawaban Soal 1 sampai 3 |
| C | Menghubungkan Python ke MySQL | 20 | `db.py` dan `tes_koneksi.py` jalan |
| D | Kerangka aplikasi, menu 1 dan 2 | 10 | Menu proyek dan tugas tampil |
| E | Menu 3 dan 4 | 15 | Bisa menambah tugas dan mengubah status |
| F | Menu 5 dan 6 | 15 | Bisa menghapus tugas dan melihat laporan |
| G | Coba sendiri | 10 | Uji keamanan, plus bonus |
| H | Simpan ke Git dan GitHub | 5 | Pekerjaan ter-push |

## Aturan main

1. Ikuti bagian dari A sampai H, berurutan.
2. Ketik hanya isi kotak berlabel **Ketik** atau **Isi file**. Sisanya dibaca saja.
3. Setiap bagian ditutup **Titik cek**. Cocok? Lanjut.
4. Tertinggal? Pakai **Jalur kejar** di bagian bawah, tidak perlu menunggu siapa pun.
5. Stuck? Tulis di grup: ID, bagian, dan tempel pesan error. Contoh: "P08 stuck di C3".
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

Ingat dua tempat mengetik yang berbeda: **terminal** (`nama@LAPTOP:~/...$`) dan **di dalam MySQL** (`mysql>`). Perintah SQL diakhiri titik koma `;`.

**Perintah SQL yang panjang** ditulis beberapa baris di lembar ini. Ketik baris pertama, tekan Enter, lalu ketik baris berikutnya. Prompt berubah jadi `->`, itu normal: MySQL menunggu sampai ketemu `;` di baris terakhir, baru menjalankannya.

**Password MySQL** adalah `sakura123`. Hurufnya tidak tampil saat diketik, itu normal.

### Kamus mini

Penjelasannya akan disampaikan trainer sambil mengetik. Tabel ini untuk dibuka kalau kamu ketemu kata yang belum kamu pahami.

| Kata | Artinya | Contoh |
| --- | --- | --- |
| JOIN | Menyambungkan baris dari dua tabel lewat kolom yang saling menunjuk | `JOIN projects p ON p.id = t.project_id` |
| LEFT JOIN | JOIN yang tetap menampilkan semua baris tabel di sebelah kiri, walau tidak punya pasangan | `FROM projects p LEFT JOIN tasks t ...` |
| Alias | Nama pendek untuk tabel atau kolom | `tasks t`, `AS proyek` |
| `GROUP BY` | Mengelompokkan baris, lalu menghitung per kelompok | `GROUP BY p.id` |
| `NULL` | Kosong, bukan angka 0 dan bukan teks kosong | `due_date` yang belum diisi |
| Pustaka | Kumpulan kode buatan orang lain yang kita pasang dan pakai | `mysql-connector-python` |
| Fungsi | Potongan kode bernama yang bisa dipanggil berulang | `def tampilkan_proyek():` |
| Dictionary | Data berpasangan nama dan nilai | `baris["title"]` |
| `commit` | Perintah "simpan permanen" ke database. Tanpa ini perubahan hilang | `conn.commit()` |
| SQL injection | Serangan lewat teks yang diketik pengguna, supaya database menjalankan perintah yang bukan miliknya | judul tugas `x'); DROP TABLE tasks; --` |

### Kalau kamu tertinggal

Buka **Titik cek** terakhir yang berhasil kamu lewati, cocokkan hasilmu, lalu lanjut. Kalau sudah lebih dari satu bagian tertinggal, pakai **Jalur kejar** di bagian bawah, termasuk `main.py` lengkap.

---

## Bagian A — Persiapan dan reset data (10 menit)

### A1 — Buka terminal dan nyalakan MySQL

Buka aplikasi **Ubuntu** dari menu Windows.

**Ketik di terminal:**

```text
sudo service mysql start
```

Kalau diminta password, itu password Ubuntu-mu.

### A2 — Masuk ke folder kerjamu dan buka VS Code

**Ketik di terminal** (ganti `p00` dengan ID-mu):

```text
cd ~/seti-isd-materi/minggu-03-database/sakura-tasks-p00
```

```text
code .
```

**Yang harus muncul di layar:** VS Code terbuka di folder `sakura-tasks-p00`, tertulis **WSL: Ubuntu** di pojok kiri bawah. Buka terminal di dalam VS Code dengan `Ctrl` dan tombol backtick (karakter di kiri angka 1). Mulai sekarang semua perintah diketik di terminal VS Code itu.

### A3 — Kembalikan data ke keadaan awal

Kemarin datamu sudah diubah-ubah oleh misi. Supaya semua peserta mulai dari data yang sama, jalankan lagi dua file kemarin.

**Folder:** `sakura-tasks-p00`

**Ketik di terminal** (ganti `p00` dengan ID-mu):

```text
mysql -u sakura_p00 -p sakura_db < db/schema.sql
```

```text
mysql -u sakura_p00 -p sakura_db < db/seed.sql
```

**Yang harus muncul di layar:** tidak ada tulisan apa-apa di keduanya (artinya berhasil).

### A4 — Cek datanya

**Ketik di terminal:**

```text
mysql -u sakura_p00 -p sakura_db
```

**Ketik di `mysql>`:**

```text
SELECT COUNT(*) FROM tasks;
```

**Yang harus muncul di layar:** angka `8`.

### A5 — Tambah satu proyek yang belum punya tugas

Proyek ini dipakai untuk melihat perbedaan jenis JOIN.

**Ketik di `mysql>`:**

```text
INSERT INTO projects (name, client) VALUES ('Portal Alumni Kampus', 'Kampus Merdeka');
```

**Ketik di `mysql>`:**

```text
SELECT * FROM projects;
```

**Yang harus muncul di layar:** 4 baris. `Portal Alumni Kampus` punya `id` 4.

### Titik cek A

- [ ] Tugas berjumlah 8
- [ ] Proyek berjumlah 4, termasuk `Portal Alumni Kampus`

---

## Bagian B — JOIN (30 menit)

Tetap di dalam MySQL.

### B1 — Masalahnya

**Ketik di `mysql>`:**

```text
SELECT title, status, project_id FROM tasks;
```

**Yang harus muncul di layar:** 8 baris. Kolom `project_id` hanya berisi angka. Nama proyeknya ada di tabel lain, yaitu `projects`.

**JOIN** menyambungkan baris dari dua tabel berdasarkan kolom yang saling menunjuk. Di tabel kita: `tasks.project_id` cocok dengan `projects.id`.

### B2 — JOIN pertama

**Ketik di `mysql>`** (tiga baris, Enter di tiap akhir baris):

```text
SELECT tasks.title, tasks.status, projects.name
FROM tasks
JOIN projects ON projects.id = tasks.project_id;
```

**Yang harus muncul di layar:** 8 baris. Tiap tugas sekarang disertai nama proyeknya. Proyek `Portal Alumni Kampus` tidak muncul karena belum punya tugas.

Cara membacanya: "Ambil tiap tugas, cari proyek yang `id`-nya sama dengan `project_id` tugas itu, lalu gabungkan keduanya dalam satu baris."

### B3 — Memperpendek dengan alias

Menulis `tasks.` dan `projects.` berulang-ulang melelahkan. Kita beri nama pendek (alias): `t` untuk `tasks`, `p` untuk `projects`, dan `AS proyek` mengganti judul kolom di hasilnya.

**Ketik di `mysql>`** (empat baris):

```text
SELECT t.title, t.status, p.name AS proyek
FROM tasks t
JOIN projects p ON p.id = t.project_id
ORDER BY p.name, t.priority;
```

**Yang harus muncul di layar:** 8 baris, tersusun per nama proyek, dengan judul kolom ketiga `proyek`.

### B4 — JOIN dengan filter

**Ketik di `mysql>`** (lima baris):

```text
SELECT t.title, p.client, t.due_date
FROM tasks t
JOIN projects p ON p.id = t.project_id
WHERE t.status = 'todo'
ORDER BY t.due_date;
```

**Yang harus muncul di layar:** 4 baris, dengan urutan:

| title | client | due_date |
| --- | --- | --- |
| Notifikasi orang tua | SD Harapan | NULL |
| Fitur keranjang belanja | Kopi Nusantara | 2026-11-25 |
| Rekap absensi bulanan | SD Harapan | 2026-11-30 |
| Layar panggilan pasien | Klinik Sehat | 2026-12-05 |

Tugas yang tenggatnya kosong (`NULL`) muncul paling atas kalau diurutkan naik.

### B5 — Dua jenis JOIN

Tabel ini dibaca saja:

| Jenis | Aturannya |
| --- | --- |
| `JOIN` (nama lengkapnya `INNER JOIN`) | Hanya baris yang punya pasangan di kedua tabel |
| `LEFT JOIN` | Semua baris dari tabel di sebelah kiri, walaupun tidak punya pasangan. Kolom pasangannya diisi `NULL` |

### B6 — Mencoba LEFT JOIN

**Ketik di `mysql>`** (empat baris):

```text
SELECT p.name, t.title
FROM projects p
LEFT JOIN tasks t ON t.project_id = p.id
ORDER BY p.id;
```

**Yang harus muncul di layar:** 9 baris. Baris terakhir: `Portal Alumni Kampus` dengan `NULL` di kolom `title`.

### B7 — Mencari proyek yang belum punya tugas

**Ketik di `mysql>`** (empat baris):

```text
SELECT p.name
FROM projects p
LEFT JOIN tasks t ON t.project_id = p.id
WHERE t.id IS NULL;
```

**Yang harus muncul di layar:** 1 baris, `Portal Alumni Kampus`.

### B8 — JOIN sambil menghitung

**Ketik di `mysql>`** (lima baris):

```text
SELECT p.name, COUNT(t.id) AS jumlah_tugas
FROM projects p
LEFT JOIN tasks t ON t.project_id = p.id
GROUP BY p.id, p.name
ORDER BY p.id;
```

**Yang harus muncul di layar:** 4 baris:

| name | jumlah_tugas |
| --- | --- |
| Toko Online Kopi Nusantara | 3 |
| Aplikasi Absensi Sekolah | 3 |
| Sistem Antrean Klinik | 2 |
| Portal Alumni Kampus | 0 |

Sekarang ketik ulang perintah yang sama, tapi ganti `COUNT(t.id)` menjadi `COUNT(*)`:

**Ketik di `mysql>`** (lima baris):

```text
SELECT p.name, COUNT(*) AS jumlah_tugas
FROM projects p
LEFT JOIN tasks t ON t.project_id = p.id
GROUP BY p.id, p.name
ORDER BY p.id;
```

**Yang harus muncul di layar:** angka untuk `Portal Alumni Kampus` berubah menjadi `1`, padahal proyek itu tidak punya tugas. Pikirkan: `COUNT(t.id)` menghitung apa, dan `COUNT(*)` menghitung apa? Trainer akan membahasnya.

### B9 — Latihan JOIN: Soal 1 sampai 3

Keluar dari MySQL dulu:

**Ketik di `mysql>`:**

```text
EXIT;
```

Buat file jawabanmu.

**Folder:** `sakura-tasks-p00`

**File:** `db/join.sql` (baru)

Di panel kiri VS Code, klik kanan folder `db`, pilih **New File**, ketik `join.sql`, lalu Enter. Tulis jawaban tiap soal di file itu, diawali komentar `-- Soal 1`, `-- Soal 2`, dan `-- Soal 3`. Coba dulu di `mysql>`, lalu salin yang benar ke file dan simpan dengan `Ctrl+S`.

> **Soal 1.** Mas Bayu: "Tugas apa saja yang sedang dikerjakan?"

Tulis satu perintah `SELECT` dengan ketentuan ini:

1. Dari tabel `tasks` (alias `t`), JOIN dengan tabel `projects` (alias `p`).
2. Tampilkan kolom `t.title`, `p.name`, dan `p.client`.
3. Tampilkan hanya baris yang `status`-nya `doing`.

Hasil yang benar: 2 baris, yaitu Integrasi pembayaran dan Nomor antrean otomatis.

> **Soal 2.** Mas Bayu: "Saya mau lihat semua tugas prioritas 1, lengkap dengan nama proyeknya."

Tulis satu perintah `SELECT` dengan ketentuan ini:

1. Dari tabel `tasks` (alias `t`), JOIN dengan tabel `projects` (alias `p`).
2. Tampilkan kolom `t.title`, `p.name`, dan `t.due_date`.
3. Tampilkan hanya baris yang `priority`-nya `1`.
4. Urutkan berdasarkan `t.due_date` dari tanggal terlama ke terbaru.

Hasil yang benar: 3 baris, dimulai dari Desain halaman produk.

> **Soal 3.** Mas Bayu: "Tiap proyek sudah menyelesaikan berapa tugas? Proyek yang belum menyelesaikan satu pun tetap harus muncul dengan angka 0."

Tulis satu perintah `SELECT` dengan ketentuan ini:

1. Dari tabel `projects` (alias `p`), `LEFT JOIN` dengan tabel `tasks` (alias `t`).
2. Tampilkan `p.name` dan jumlah tugas selesai dengan nama kolom `jumlah_selesai`.
3. Kelompokkan dengan `GROUP BY p.id, p.name`, dan urutkan dengan `ORDER BY p.id`.

Hasil yang benar: 4 baris dengan angka 1, 1, 0, 0.

Petunjuk Soal 3: ini jebakan. Kalau kamu menaruh `t.status = 'done'` di `WHERE`, proyek yang belum punya tugas selesai hilang dari hasil. Coba letakkan syarat itu di `ON`, setelah `AND`. Jawaban lengkap ada di Jalur kejar kalau kamu buntu.

### Titik cek B

- [ ] B2 menghasilkan 8 baris dan B6 menghasilkan 9 baris
- [ ] B7 menghasilkan 1 baris, `Portal Alumni Kampus`
- [ ] Angka `Portal Alumni Kampus` di B8 berubah dari `0` menjadi `1` saat `COUNT(t.id)` diganti `COUNT(*)`
- [ ] `db/join.sql` berisi jawaban Soal 1 sampai 3

---

## Bagian C — Menghubungkan Python ke MySQL (20 menit)

### C1 — Buat proyek Python dengan uv

Seperti minggu lalu, kita memakai `uv`. Folder `sakura-tasks-p00` milikmu diubah menjadi proyek Python.

**Folder:** `~/seti-isd-materi/minggu-03-database/sakura-tasks-p00`

**Ketik di terminal:**

```text
uv init --no-package --vcs none --python 3.12
```

**Yang harus muncul di layar:** `Initialized project`. Di panel kiri VS Code muncul file `main.py`, `pyproject.toml`, dan `README.md`.

Arti `--vcs none`: jangan membuat repo Git baru, karena folder ini sudah berada di dalam repo `seti-isd-materi`. Arti `--no-package`: sama seperti minggu lalu.

### C2 — Pasang pustaka penghubung ke MySQL

**Ketik di terminal:**

```text
uv add mysql-connector-python
```

**Yang harus muncul di layar:** beberapa baris yang memuat `Resolved` dan `Installed`. Pertama kali, beberapa baris lain tentang menyiapkan lingkungan bisa muncul. Abaikan. File `pyproject.toml` sekarang menyebut `mysql-connector-python` di bagian `dependencies`.

### C3 — Cegah file sampah ikut ke Git

Folder `.venv` dan `__pycache__` tidak boleh ikut masuk ke Git.

**Ketik di terminal:**

```text
echo ".venv/" >> .gitignore
```

```text
echo "__pycache__/" >> .gitignore
```

### C4 — Buat db.py

Satu file khusus untuk urusan koneksi, supaya bagian lain aplikasi tidak perlu tahu cara tersambung ke database.

**Folder:** `sakura-tasks-p00`

**File:** `db.py` (baru). Letaknya langsung di folder `sakura-tasks-p00`, **bukan** di dalam folder `db`.

Di panel kiri VS Code, klik kanan pada ruang kosong di bawah daftar file, pilih **New File**, ketik `db.py`, lalu Enter.

**Isi file** (tempel, ganti `p00` pada baris `"user"` dengan ID-mu, lalu simpan dengan `Ctrl+S`):

```python
import mysql.connector

DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "sakura_p00",
    "password": "sakura123",
    "database": "sakura_db",
}


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def fetch_all(sql, params=()):
    conn = get_connection()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, params)
        return cur.fetchall()
    finally:
        conn.close()


def execute(sql, params=()):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        return cur.rowcount
    finally:
        conn.close()
```

Kegunaan tiap fungsi (dibaca saja):

| Fungsi | Untuk |
| --- | --- |
| `get_connection()` | Membuka sambungan ke database |
| `fetch_all(sql, params)` | Menjalankan `SELECT`, mengembalikan daftar baris. Tiap baris berupa dictionary, jadi bisa dibaca dengan `baris["title"]` |
| `execute(sql, params)` | Menjalankan `INSERT`, `UPDATE`, atau `DELETE`, lalu mengembalikan jumlah baris yang kena |

Perhatikan `conn.commit()` di `execute`. Tanpa `commit`, perubahan **tidak tersimpan** di database. Ini kesalahan yang paling sering dialami pemula.

### C5 — Buat tes_koneksi.py

**Folder:** `sakura-tasks-p00`

**File:** `tes_koneksi.py` (baru, di folder `sakura-tasks-p00`, dibuat dengan cara yang sama seperti `db.py`)

**Isi file** (tempel, lalu simpan dengan `Ctrl+S`):

```python
from db import fetch_all

for baris in fetch_all("SELECT COUNT(*) AS total FROM tasks"):
    print("Jumlah tugas:", baris["total"])
```

### C6 — Jalankan tes

**Ketik di terminal:**

```text
uv run tes_koneksi.py
```

**Yang harus muncul di layar:**

```text
Jumlah tugas: 8
```

Kalau muncul error, lihat tabel "Masalah yang sering muncul" di bagian bawah.

### C7 — Aturan penting: jangan sambung teks SQL sendiri

Bagian ini dibaca saja. Perhatikan `fetch_all(sql, params)` punya parameter `params`. Kalau SQL-nya butuh nilai dari pengguna, tulis `%s` di SQL dan taruh nilainya di `params`. Contoh:

```python
fetch_all("SELECT * FROM tasks WHERE status = %s", ("todo",))
```

**Jangan** menyambung nilainya langsung ke teks SQL, misalnya dengan f-string:

```python
fetch_all(f"SELECT * FROM tasks WHERE status = '{status}'")
```

Alasannya: kalau pengguna mengetik teks yang berisi tanda kutip dan perintah SQL, perintahnya ikut dijalankan. Serangan ini disebut **SQL injection**, dan masih jadi salah satu penyebab kebocoran data paling umum. Dengan `%s`, pustaka yang mengamankan nilainya. Di aplikasi ini kita **selalu** pakai `%s`.

Catatan: menaruh password di dalam kode seperti `db.py` hanya untuk latihan di laptop sendiri. Di aplikasi sungguhan, password disimpan di luar kode.

### Titik cek C

- [ ] `uv run tes_koneksi.py` menampilkan `Jumlah tugas: 8`
- [ ] File `db.py` dan `tes_koneksi.py` ada langsung di folder `sakura-tasks-p00`
- [ ] `pyproject.toml` menyebut `mysql-connector-python`

---

## Bagian D — Kerangka aplikasi, menu 1 dan 2 (10 menit)

File utamanya sudah ada: `main.py`, dibuat oleh `uv init` dan berisi contoh bawaan.

### D1 — Ganti isi main.py

**Folder:** `sakura-tasks-p00`

**File:** `main.py` (sudah ada)

Di panel kiri VS Code, klik `main.py`, tekan `Ctrl+A` lalu `Delete` untuk mengosongkannya.

**Isi file** (tempel, lalu simpan dengan `Ctrl+S`). Menu 1 dan 2 sudah jadi. Menu 3 sampai 6 masih berisi tulisan "Fitur ini belum dibuat", dan itu diisi di Bagian E dan F:

```python
import mysql.connector

from db import fetch_all, execute


def tampilkan_proyek():
    rows = fetch_all("SELECT id, name, client FROM projects ORDER BY id")
    print("\n=== Daftar Proyek ===")
    for r in rows:
        print(f"{r['id']}. {r['name']} (klien: {r['client']})")


def tampilkan_tugas():
    sql = """
        SELECT t.id, t.title, t.status, t.priority, p.name AS project_name
        FROM tasks t
        JOIN projects p ON p.id = t.project_id
        ORDER BY t.priority, t.id
    """
    rows = fetch_all(sql)
    print("\n=== Daftar Tugas ===")
    for r in rows:
        print(
            f"[{r['id']}] {r['title']} | {r['status']} | "
            f"P{r['priority']} | {r['project_name']}"
        )


def tambah_tugas():
    print("Fitur ini belum dibuat (menu 3)")


def ubah_status():
    print("Fitur ini belum dibuat (menu 4)")


def hapus_tugas():
    print("Fitur ini belum dibuat (menu 5)")


def laporan():
    print("Fitur ini belum dibuat (menu 6)")


MENU = """
=== Sakura Tasks ===
1. Lihat proyek
2. Lihat tugas
3. Tambah tugas
4. Ubah status tugas
5. Hapus tugas
6. Laporan jumlah tugas per proyek
0. Keluar
"""

AKSI = {
    "1": tampilkan_proyek,
    "2": tampilkan_tugas,
    "3": tambah_tugas,
    "4": ubah_status,
    "5": hapus_tugas,
    "6": laporan,
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

### D2 — Jalankan

**Ketik di terminal:**

```text
uv run main.py
```

**Yang harus muncul di layar:** menu `=== Sakura Tasks ===`.

Di `Pilih menu:`, ketik `1` lalu Enter. **Yang harus muncul:** 4 proyek. Ketik `2` lalu Enter. **Yang harus muncul:** 8 tugas lengkap dengan nama proyeknya. Menu 2 itulah hasil JOIN yang diminta Mas Bayu. Ketik `0` lalu Enter untuk keluar.

### D3 — Pelajari polanya

Dibaca saja. Pola yang sama dipakai di semua menu berikutnya:

| Bagian kode | Fungsinya |
| --- | --- |
| `fetch_all(sql)` | Mengambil baris dari database lewat `SELECT` |
| `for r in rows:` | Mengulang untuk tiap baris |
| `r['title']` | Mengambil isi kolom `title` dari satu baris |
| `AKSI = {...}` | Daftar yang mencocokkan nomor menu dengan fungsinya |
| `try: ... except mysql.connector.Error` | Kalau database bermasalah, tampilkan pesan rapi, bukan error panjang |

### Titik cek D

- [ ] Menu 1 menampilkan 4 proyek
- [ ] Menu 2 menampilkan 8 tugas dengan nama proyek
- [ ] Menu 3 sampai 6 menampilkan "Fitur ini belum dibuat"

---

## Bagian E — Menu 3 dan 4: tambah tugas dan ubah status (15 menit)

Kali ini kamu mengganti dua fungsi di `main.py`. Setiap kali, caranya sama: cari fungsi yang lama, hapus, lalu tempel fungsi baru **di tempat yang sama**. Jangan sampai ada dua fungsi dengan nama yang sama di `main.py`.

### E1 — Fungsi tambah_tugas (menu 3)

**File:** `main.py`

Cari dua baris ini dan **hapus keduanya**:

```python
def tambah_tugas():
    print("Fitur ini belum dibuat (menu 3)")
```

**Isi file:** tempel ini di tempat yang sama:

```python
def tambah_tugas():
    tampilkan_proyek()
    project_id = input("Nomor proyek: ").strip()
    judul = input("Judul tugas: ").strip()
    prioritas = input("Prioritas 1-3 (kosongkan untuk 2): ").strip()
    if not project_id.isdigit():
        print("Nomor proyek harus angka.")
        return
    if judul == "":
        print("Judul tugas tidak boleh kosong.")
        return
    if prioritas == "":
        prioritas = "2"
    if prioritas not in ("1", "2", "3"):
        print("Prioritas harus 1, 2, atau 3.")
        return
    execute(
        "INSERT INTO tasks (project_id, title, priority) VALUES (%s, %s, %s)",
        (project_id, judul, prioritas),
    )
    print(f"Tugas '{judul}' berhasil disimpan.")
```

### E2 — Fungsi ubah_status (menu 4)

**File:** `main.py`

Cari dua baris ini dan **hapus keduanya**:

```python
def ubah_status():
    print("Fitur ini belum dibuat (menu 4)")
```

**Isi file:** tempel ini di tempat yang sama:

```python
def ubah_status():
    tampilkan_tugas()
    nomor = input("Nomor tugas: ").strip()
    status = input("Status baru (todo/doing/done): ").strip()
    if not nomor.isdigit():
        print("Nomor tugas harus angka.")
        return
    if status not in ("todo", "doing", "done"):
        print("Status harus todo, doing, atau done.")
        return
    ada = fetch_all("SELECT id FROM tasks WHERE id = %s", (nomor,))
    if not ada:
        print("Tugas tidak ditemukan.")
        return
    execute("UPDATE tasks SET status = %s WHERE id = %s", (status, nomor))
    print("Status tugas berhasil diubah.")
```

Simpan dengan `Ctrl+S`.

### E3 — Uji menu 3 dan 4

**Ketik di terminal:**

```text
uv run main.py
```

Uji menu 3 (ketik jawaban di tiap pertanyaan, Enter setelahnya):

| Pertanyaan di layar | Ketik |
| --- | --- |
| `Pilih menu:` | `3` |
| `Nomor proyek:` | `4` |
| `Judul tugas:` | `Desain halaman beranda` |
| `Prioritas 1-3 (kosongkan untuk 2):` | `1` |

**Yang harus muncul di layar:** `Tugas 'Desain halaman beranda' berhasil disimpan.`

Ketik `2` di `Pilih menu:`. **Yang harus muncul:** tugas berjumlah 9, dan tugas baru itu tampil dengan prioritas P1 dan proyek `Portal Alumni Kampus`.

Uji menu 4:

| Pertanyaan di layar | Ketik |
| --- | --- |
| `Pilih menu:` | `4` |
| `Nomor tugas:` | `2` |
| `Status baru (todo/doing/done):` | `done` |

**Yang harus muncul di layar:** `Status tugas berhasil diubah.` Lalu menu 2 menampilkan tugas nomor 2 berstatus `done`.

Uji penolakan. Ketik `4`, lalu nomor tugas `999`, lalu status `done`. **Yang harus muncul:** `Tugas tidak ditemukan.` Ketik `4`, nomor `2`, status `selesai`. **Yang harus muncul:** `Status harus todo, doing, atau done.`

Ketik `0` untuk keluar.

### Titik cek E

- [ ] Menu 3 menyimpan tugas baru dan menu 2 menampilkannya, lengkap dengan nama proyek
- [ ] Menu 4 mengubah status, dan menu 2 menampilkan status barunya
- [ ] Nomor tugas yang tidak ada ditolak dengan `Tugas tidak ditemukan.`
- [ ] Status selain `todo`, `doing`, `done` ditolak
- [ ] Tekan `Ctrl+F` di `main.py`, cari `belum dibuat`: tinggal 2 hasil (menu 5 dan 6)

---

## Bagian F — Menu 5 dan 6: hapus tugas dan laporan (15 menit)

### F1 — Fungsi hapus_tugas (menu 5)

**File:** `main.py`

Cari dua baris ini dan **hapus keduanya**:

```python
def hapus_tugas():
    print("Fitur ini belum dibuat (menu 5)")
```

**Isi file:** tempel ini di tempat yang sama:

```python
def hapus_tugas():
    tampilkan_tugas()
    nomor = input("Nomor tugas yang dihapus: ").strip()
    if not nomor.isdigit():
        print("Nomor tugas harus angka.")
        return
    baris = fetch_all("SELECT title FROM tasks WHERE id = %s", (nomor,))
    if not baris:
        print("Tugas tidak ditemukan.")
        return
    jawab = input(f"Yakin hapus '{baris[0]['title']}'? (y/n): ").strip().lower()
    if jawab != "y":
        print("Dibatalkan.")
        return
    execute("DELETE FROM tasks WHERE id = %s", (nomor,))
    print("Tugas dihapus.")
```

### F2 — Fungsi laporan (menu 6)

**File:** `main.py`

Cari dua baris ini dan **hapus keduanya**:

```python
def laporan():
    print("Fitur ini belum dibuat (menu 6)")
```

**Isi file:** tempel ini di tempat yang sama:

```python
def laporan():
    sql = """
        SELECT p.name,
               COUNT(t.id) AS jumlah,
               COALESCE(SUM(t.status = 'done'), 0) AS selesai
        FROM projects p
        LEFT JOIN tasks t ON t.project_id = p.id
        GROUP BY p.id, p.name
        ORDER BY p.id
    """
    rows = fetch_all(sql)
    print("\n=== Laporan per Proyek ===")
    for r in rows:
        print(f"{r['name']}: {r['jumlah']} tugas, {r['selesai']} selesai")
```

Simpan dengan `Ctrl+S`. Dua hal yang dibahas trainer:

- `LEFT JOIN` membuat proyek yang belum punya tugas tetap muncul.
- Untuk proyek tanpa tugas, `SUM(...)` menghasilkan `NULL`, bukan 0. `COALESCE(..., 0)` mengganti `NULL` itu dengan 0.

### F3 — Uji menu 5 dan 6

**Ketik di terminal:**

```text
uv run main.py
```

Uji menu 6: ketik `6`. Karena kamu sudah menambah satu tugas dan mengubah satu status di Bagian E, **yang harus muncul** adalah:

```text
=== Laporan per Proyek ===
Toko Online Kopi Nusantara: 3 tugas, 2 selesai
Aplikasi Absensi Sekolah: 3 tugas, 1 selesai
Sistem Antrean Klinik: 2 tugas, 0 selesai
Portal Alumni Kampus: 1 tugas, 0 selesai
```

Uji menu 5, jawab `n` dulu:

| Pertanyaan di layar | Ketik |
| --- | --- |
| `Pilih menu:` | `5` |
| `Nomor tugas yang dihapus:` | `9` |
| `Yakin hapus 'Desain halaman beranda'? (y/n):` | `n` |

**Yang harus muncul di layar:** `Dibatalkan.` Ketik `2`: tugas nomor 9 masih ada.

Ulangi menu 5 dengan nomor `9`, tapi jawab `y`. **Yang harus muncul:** `Tugas dihapus.` Ketik `2`: tugas nomor 9 sudah hilang, tugas berjumlah 8.

Ketik `6`. **Yang harus muncul:** `Portal Alumni Kampus: 0 tugas, 0 selesai`. Proyek tanpa tugas tetap tampil dengan angka 0.

Ketik `0` untuk keluar.

### Titik cek F

- [ ] Menjawab `n` membatalkan penghapusan, menjawab `y` menghapus tugasnya
- [ ] Menu 6 menampilkan 4 proyek, termasuk yang tanpa tugas dengan angka 0
- [ ] Tekan `Ctrl+F` di `main.py`, cari `belum dibuat`: tidak ada hasil lagi

---

## Bagian G — Coba sendiri (10 menit)

### G1 — Misi: uji keamanan

Rani, anak magang di tim Mas Bayu, iseng menguji aplikasi. Dia menambah tugas dengan judul `Rapat dengan klien 'Kopi'` (ada tanda kutip di dalamnya), lalu satu lagi dengan judul `x'); DROP TABLE tasks; --`.

Lakukan hal yang sama lewat menu 3, dengan isian ini:

| Pertanyaan di layar | Ketikan pertama | Ketikan kedua |
| --- | --- | --- |
| `Nomor proyek:` | `1` | `1` |
| `Judul tugas:` | `Rapat dengan klien 'Kopi'` | `x'); DROP TABLE tasks; --` |
| `Prioritas 1-3 (kosongkan untuk 2):` | tekan Enter saja | tekan Enter saja |

Hasil yang benar: kedua judul tersimpan apa adanya, dan menu 2 tetap bisa menampilkan daftar tugas (tabel `tasks` aman).

Lalu di bagian paling atas `main.py`, tambahkan komentar (tiap baris diawali tanda `#`) yang menjawab: kenapa aplikasi ini aman dari judul semacam itu? Apa yang berbeda di kode kita dibanding menyambung teks SQL dengan f-string? Cukup satu sampai dua kalimat.

### G2 — Bonus A: cari tugas (menu 7), kalau sempat

Mas Bayu: "Saya mau mencari tugas dari satu kata."

1. Di `main.py`, tambahkan fungsi baru `cari_tugas()`. Fungsi itu bertanya `Kata kunci:`, lalu menampilkan semua tugas yang `title`-nya mengandung kata itu, lengkap dengan nama proyeknya (pakai `JOIN` seperti `tampilkan_tugas`).
2. Syarat SQL-nya memakai `WHERE t.title LIKE %s`. Tanda `%` ditaruh di nilai parameternya, bukan di teks SQL. Contoh nilainya: `f"%{kata}%"`.
3. Tambahkan baris `7. Cari tugas` di teks `MENU`, dan baris `"7": cari_tugas,` di `AKSI`.

Hasil yang benar: mengetik `absensi` menampilkan tugas Rekap absensi bulanan beserta proyeknya.

### G3 — Bonus B: anggota tim (menu 2 dengan tiga tabel), kalau sempat

Mas Bayu: "Saya ingin tahu siapa yang mengerjakan tiap tugas." Kerjakan di `mysql>`:

1. Buat tabel `members` dengan kolom `id` (primary key, terisi otomatis) dan `name` (teks, wajib diisi).
2. Tambahkan kolom `member_id` bertipe `INT` yang boleh kosong ke tabel `tasks` dengan `ALTER TABLE tasks ADD COLUMN ...`, lalu jadikan kolom itu foreign key ke `members.id`.
3. Isi tabel `members` dengan tiga nama, lalu isi `member_id` di beberapa tugas dengan `UPDATE`.
4. Ubah fungsi `tampilkan_tugas()` di `main.py`: tambahkan `LEFT JOIN members m ON m.id = t.member_id`, tampilkan `m.name`, dan tampilkan `-` kalau nilainya kosong.

Hasil yang benar: menu 2 menampilkan nama pengerjanya, dan tugas yang belum punya pengerja tetap tampil.

### Titik cek G

- [ ] Dua judul uji dari Rani tersimpan apa adanya dan menu 2 masih jalan
- [ ] Komentar jawaban uji keamanan tertulis di bagian atas `main.py`

---

## Bagian H — Simpan ke Git dan GitHub (5 menit)

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
git commit -m "Hari 2: latihan JOIN dan aplikasi Sakura Tasks dengan MySQL"
```

```text
git pull --rebase
```

```text
git push
```

Kalian semua menyimpan ke repo yang sama, jadi `git pull --rebase` mengambil pekerjaan teman yang sudah lebih dulu dikirim. Kalau `git push` ditolak dengan tulisan `rejected` atau `fetch first`, ulangi `git pull --rebase`, lalu `git push`.

Buka repo di GitHub lewat browser, lalu pastikan folder `minggu-03-database/sakura-tasks-p00` berisi `main.py`, `db.py`, `pyproject.toml`, dan folder `db` dengan `join.sql`. Folder `.venv` tidak boleh ikut ter-upload. Kalau ikut, tulis di grup.

Catatan: `db.py` berisi password latihan, dan file itu ikut masuk ke repo. Pastikan password `sakura123` tidak kamu pakai untuk akun atau layanan lain.

### Titik cek H

- [ ] `git push` selesai tanpa error
- [ ] `main.py`, `db.py`, `pyproject.toml`, dan `db/join.sql` ada di folder milikmu di GitHub, dan folder `.venv` tidak ada

---

## Titik cek akhir Hari 2 dan jika ada masalah

### Target minimal Hari 2

- [ ] `uv run tes_koneksi.py` menampilkan jumlah tugas
- [ ] Menu 1 sampai 6 di `uv run main.py` jalan
- [ ] Menu 6 menampilkan proyek yang belum punya tugas dengan angka 0
- [ ] File `db/join.sql` berisi jawaban Soal 1 sampai 3
- [ ] Jawaban uji keamanan tertulis sebagai komentar di `main.py`
- [ ] Kamu bisa menjelaskan ke teman: apa beda `JOIN` dengan `LEFT JOIN`, dan kenapa `%s` dipakai, bukan f-string
- [ ] Pekerjaanmu sudah di-push dan terlihat di GitHub

### Masalah yang sering muncul

| Pesan error | Penyebab | Yang dilakukan |
| --- | --- | --- |
| `ModuleNotFoundError: No module named 'mysql'` | Pustaka belum dipasang, atau programnya dijalankan dengan `python` biasa, bukan `uv run` | Jalankan `uv add mysql-connector-python` dari folder `sakura-tasks-p00`, lalu jalankan dengan `uv run main.py` |
| `ModuleNotFoundError: No module named 'db'` | Kamu menjalankan dari folder yang salah, atau `db.py` tidak ada di folder itu | `cd ~/seti-isd-materi/minggu-03-database/sakura-tasks-p00`, pastikan `db.py` ada di situ |
| `command not found: uv` | `uv` belum terpasang atau terminal belum dimuat ulang | Tutup terminal, buka lagi, coba `uv --version`. Kalau tetap gagal, tulis di grup |
| `2003 (HY000): Can't connect to MySQL server` | MySQL belum menyala | `sudo service mysql start` |
| `1045 (28000): Access denied for user` | Salah user atau password di `db.py` | Cek `DB_CONFIG`: `p00` sudah diganti ID-mu, password `sakura123` |
| `1049 (42000): Unknown database` | Nama database di `db.py` salah | Pastikan `"database": "sakura_db"` |
| `1146 (42S02): Table ... doesn't exist` | `schema.sql` belum dijalankan | Jalankan ulang `schema.sql` dan `seed.sql` seperti di A3 |
| `1452 (23000): Cannot add or update a child row` | Nomor proyek yang diisi tidak ada | Cek menu 1 atau `SELECT * FROM projects;` |
| `IndentationError` atau `SyntaxError` | Salah tempel, atau spasi di awal baris tergeser | Periksa baris yang disebut di pesan error. Di Python, spasi di awal baris berarti |
| `NameError: name '...' is not defined` | Fungsi terhapus, atau salah ketik nama | Cocokkan nama fungsi dengan `AKSI` dan dengan `main.py` lengkap di Jalur kejar |
| Perubahan data hilang setelah aplikasi ditutup | Lupa `commit` | Pastikan perubahan dijalankan lewat fungsi `execute` di `db.py`, yang memanggil `conn.commit()` |
| Menu 6 tidak memuat proyek tanpa tugas | Memakai `JOIN` biasa, atau syarat diletakkan di `WHERE` | Ingat Bagian B: `LEFT JOIN`, dan beda `WHERE` dengan `ON` |
| `git push` ditolak (`rejected`, `fetch first`) | Teman sudah lebih dulu mengirim pekerjaan | `git pull --rebase`, lalu `git push` lagi |

Setelah mencoba sendiri dan bertanya ke AI atau mencari di internet masih macet? Tulis di grup.

### Jalur kejar

**Kalau Hari 1 belum selesai.** Pastikan `db/schema.sql` dan `db/seed.sql` berisi teks dari lembar Hari 1 (Bagian B1 dan C2). Lalu kerjakan Bagian A dari awal. Soal `latihan.sql` tidak dibutuhkan hari ini.

**Kalau tertinggal di Bagian B (JOIN).** Jawaban Soal 1 sampai 3 untuk `db/join.sql`, supaya kamu bisa lanjut ke Bagian C:

```sql
-- Soal 1
SELECT t.title, p.name, p.client
FROM tasks t
JOIN projects p ON p.id = t.project_id
WHERE t.status = 'doing';

-- Soal 2
SELECT t.title, p.name, t.due_date
FROM tasks t
JOIN projects p ON p.id = t.project_id
WHERE t.priority = 1
ORDER BY t.due_date;

-- Soal 3
SELECT p.name, COUNT(t.id) AS jumlah_selesai
FROM projects p
LEFT JOIN tasks t ON t.project_id = p.id AND t.status = 'done'
GROUP BY p.id, p.name
ORDER BY p.id;
```

Pelajari kenapa Soal 3 meletakkan `t.status = 'done'` di `ON`, bukan di `WHERE`.

**Kalau tertinggal di Bagian D sampai F.** Ganti seluruh isi `main.py` dengan versi lengkap berikut (klik `main.py`, `Ctrl+A`, `Delete`, tempel, `Ctrl+S`). Pastikan Bagian C (`db.py`) sudah jalan. Lalu lompat ke uji di E3, F3, dan lanjut ke Bagian G.

```python
import mysql.connector

from db import fetch_all, execute


def tampilkan_proyek():
    rows = fetch_all("SELECT id, name, client FROM projects ORDER BY id")
    print("\n=== Daftar Proyek ===")
    for r in rows:
        print(f"{r['id']}. {r['name']} (klien: {r['client']})")


def tampilkan_tugas():
    sql = """
        SELECT t.id, t.title, t.status, t.priority, p.name AS project_name
        FROM tasks t
        JOIN projects p ON p.id = t.project_id
        ORDER BY t.priority, t.id
    """
    rows = fetch_all(sql)
    print("\n=== Daftar Tugas ===")
    for r in rows:
        print(
            f"[{r['id']}] {r['title']} | {r['status']} | "
            f"P{r['priority']} | {r['project_name']}"
        )


def tambah_tugas():
    tampilkan_proyek()
    project_id = input("Nomor proyek: ").strip()
    judul = input("Judul tugas: ").strip()
    prioritas = input("Prioritas 1-3 (kosongkan untuk 2): ").strip()
    if not project_id.isdigit():
        print("Nomor proyek harus angka.")
        return
    if judul == "":
        print("Judul tugas tidak boleh kosong.")
        return
    if prioritas == "":
        prioritas = "2"
    if prioritas not in ("1", "2", "3"):
        print("Prioritas harus 1, 2, atau 3.")
        return
    execute(
        "INSERT INTO tasks (project_id, title, priority) VALUES (%s, %s, %s)",
        (project_id, judul, prioritas),
    )
    print(f"Tugas '{judul}' berhasil disimpan.")


def ubah_status():
    tampilkan_tugas()
    nomor = input("Nomor tugas: ").strip()
    status = input("Status baru (todo/doing/done): ").strip()
    if not nomor.isdigit():
        print("Nomor tugas harus angka.")
        return
    if status not in ("todo", "doing", "done"):
        print("Status harus todo, doing, atau done.")
        return
    ada = fetch_all("SELECT id FROM tasks WHERE id = %s", (nomor,))
    if not ada:
        print("Tugas tidak ditemukan.")
        return
    execute("UPDATE tasks SET status = %s WHERE id = %s", (status, nomor))
    print("Status tugas berhasil diubah.")


def hapus_tugas():
    tampilkan_tugas()
    nomor = input("Nomor tugas yang dihapus: ").strip()
    if not nomor.isdigit():
        print("Nomor tugas harus angka.")
        return
    baris = fetch_all("SELECT title FROM tasks WHERE id = %s", (nomor,))
    if not baris:
        print("Tugas tidak ditemukan.")
        return
    jawab = input(f"Yakin hapus '{baris[0]['title']}'? (y/n): ").strip().lower()
    if jawab != "y":
        print("Dibatalkan.")
        return
    execute("DELETE FROM tasks WHERE id = %s", (nomor,))
    print("Tugas dihapus.")


def laporan():
    sql = """
        SELECT p.name,
               COUNT(t.id) AS jumlah,
               COALESCE(SUM(t.status = 'done'), 0) AS selesai
        FROM projects p
        LEFT JOIN tasks t ON t.project_id = p.id
        GROUP BY p.id, p.name
        ORDER BY p.id
    """
    rows = fetch_all(sql)
    print("\n=== Laporan per Proyek ===")
    for r in rows:
        print(f"{r['name']}: {r['jumlah']} tugas, {r['selesai']} selesai")


MENU = """
=== Sakura Tasks ===
1. Lihat proyek
2. Lihat tugas
3. Tambah tugas
4. Ubah status tugas
5. Hapus tugas
6. Laporan jumlah tugas per proyek
0. Keluar
"""

AKSI = {
    "1": tampilkan_proyek,
    "2": tampilkan_tugas,
    "3": tambah_tugas,
    "4": ubah_status,
    "5": hapus_tugas,
    "6": laporan,
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

**Kalau datamu berantakan dan ingin mengulang dari awal.** Ulangi A3 (`schema.sql`, lalu `seed.sql`) dan A5 (proyek `Portal Alumni Kampus`).
