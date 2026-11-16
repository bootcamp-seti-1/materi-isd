# Hari 1 (Selasa) — Hands-on: schema dan CRUD di MySQL

Ikuti langkahnya berurutan, ketik persis, dan cocokkan hasilmu di setiap titik cek. Penjelasan disampaikan trainer sambil mengetik. Hari ini belum ada Python. Semuanya di database.

## Tujuan 3 hari

Di akhir Hari 3, kamu punya dua aplikasi yang menyimpan datanya di MySQL, bukan di file:

| Hari | Hasil di akhir hari |
| --- | --- |
| Hari 1 (hari ini) | Dua tabel `projects` dan `tasks` di database `sakura_db`, terisi data, dan kamu bisa menambah, melihat, mengubah, dan menghapus datanya lewat SQL |
| Hari 2 | Menggabungkan dua tabel dengan JOIN, lalu aplikasi menu `Sakura Tasks` di Python yang memakai MySQL |
| Hari 3 | Aplikasi sistem perpustakaan SD Harapan dengan tiga tabel dan lima menu |

### Hasil akhir yang dikejar hari ini

Isi folder kerjamu (ID-mu menggantikan `p00`):

```text
sakura-tasks-p00/
  db/
    schema.sql      rancangan tabel
    seed.sql        data awal
    latihan.sql     jawaban misi
```

Dan di MySQL:

```text
mysql> SELECT COUNT(*) FROM projects;
mysql> SELECT COUNT(*) FROM tasks;
```

menghasilkan angka yang sama dengan titik cek di akhir lembar ini.

### Cerita singkat

PT Sakura Soft mencatat proyek dan tugas timnya di file teks. Kalau dua orang mengedit bersamaan, datanya bisa tertimpa. Mas Bayu (tim lead) memutuskan datanya dipindah ke database. Tugasmu hari ini: membuat tempat penyimpanannya, lalu belajar mengelola isinya.

## Persiapan sebelum mulai

- [ ] Laptop terhubung internet dan baterai aman untuk 2 jam
- [ ] Aplikasi **Ubuntu** terbuka dari menu Windows (bukan PowerShell)
- [ ] MySQL sudah terpasang dan user `sakura_` diikuti ID-mu sudah dibuat (dari materi instalasi MySQL)
- [ ] VS Code terpasang beserta ekstensi WSL (sama seperti minggu lalu)
- [ ] Repo `seti-isd-materi` sudah ada di laptopmu, di folder `~/seti-isd-materi`
- [ ] Aku tahu ID pesertaku, ditulis huruf kecil (contoh: `p01`)

## Peta Hari 1 (115 menit)

| Bagian | Isi | Menit | Hasilnya |
| --- | --- | --- | --- |
| A | Persiapan | 10 | MySQL menyala, folder kerja siap, VS Code terbuka |
| B | Membuat schema | 20 | Tabel `projects` dan `tasks` ada |
| C | Mengisi data awal | 10 | 3 proyek dan 8 tugas |
| D | Melihat data (`SELECT`) | 20 | Bisa memfilter, mengurutkan, menghitung |
| E | Menambah, mengubah, menghapus | 20 | `INSERT`, `UPDATE`, `DELETE` |
| F | Misi 1 sampai 6 | 25 | `db/latihan.sql` terisi |
| G | Simpan ke Git dan GitHub | 10 | Pekerjaan ter-push |

## Aturan main

1. Ikuti bagian dari A sampai G, berurutan.
2. Ketik hanya isi kotak berlabel **Ketik** atau **Isi file**. Sisanya dibaca saja.
3. Setiap bagian ditutup **Titik cek**. Cocok? Lanjut.
4. Tertinggal? Pakai **Jalur kejar** di bagian bawah, tidak perlu menunggu siapa pun.
5. Stuck? Tulis di grup: ID, bagian, dan tempel pesan error. Contoh: "P08 stuck di B3".
6. Boleh bertanya ke AI atau mencari di internet. Tapi kamu harus bisa menjelaskan sendiri apa yang kamu ketik.

## Cara membaca lembar ini

| Label | Artinya |
| --- | --- |
| **Folder** | Tempat kamu harus berada saat mengetik |
| **File** | Nama file beserta lokasinya. "Baru" berarti kamu yang membuatnya |
| **Isi file** | Teks yang ditempel ke dalam file di VS Code, lalu disimpan dengan `Ctrl+S` |
| **Ketik di terminal** | Perintah yang diketik di terminal Ubuntu, yaitu baris yang berakhir dengan `$` |
| **Ketik di `mysql>`** | Perintah yang diketik setelah masuk ke MySQL, yaitu baris yang diawali `mysql>` |
| **Yang harus muncul di layar** | Hanya dibaca. Jangan diketik |
| **Titik cek** | Cocokkan hasilmu sebelum lanjut |

Ada dua tempat mengetik yang berbeda, jangan tertukar:

| Tempat | Tanda di layar | Contoh isinya |
| --- | --- | --- |
| Terminal | `nama@LAPTOP:~/...$` | `cd ~/seti-isd-materi`, `mysql -u sakura_p00 -p sakura_db` |
| Di dalam MySQL | `mysql>` | `SELECT * FROM tasks;`, `EXIT;` |

Perintah SQL (yang diketik di `mysql>`) selalu diakhiri tanda titik koma `;`. Kalau lupa, prompt berubah menjadi `->` dan MySQL menunggu. Ketik `;` lalu Enter.

**Contoh salah dan benar.** Kalau lembar menyuruh melihat semua tugas, yang diketik hanya ini:

```text
SELECT * FROM tasks;
```

Kalimat penjelasan di sekitarnya dibaca saja, tidak ikut diketik.

**Password MySQL.** Tiap kali perintah `mysql -u ... -p` dijalankan, muncul tulisan `Enter password:`. Ketik `sakura123` lalu Enter. Huruf yang kamu ketik **tidak tampil di layar**, itu normal.

### Kamus mini

Penjelasannya akan disampaikan trainer sambil mengetik. Tabel ini untuk dibuka kalau kamu ketemu kata yang belum kamu pahami.

| Kata | Artinya | Contoh |
| --- | --- | --- |
| Database | Tempat menyimpan semua tabel | `sakura_db` |
| Tabel | Satu kumpulan data sejenis, bentuknya seperti satu sheet Excel | `projects`, `tasks` |
| Kolom | Satu judul kolom di tabel, menentukan jenis datanya | `title`, `status` |
| Baris (row) | Satu data lengkap di tabel | satu tugas |
| Schema | Rancangan tabel: tabel apa saja, kolom apa saja, tipe datanya apa | semua `CREATE TABLE` kita |
| Primary key (PK) | Kolom yang nilainya unik untuk tiap baris | `id` |
| Foreign key (FK) | Kolom yang berisi PK dari tabel lain, jadi penghubung antar tabel | `tasks.project_id` berisi `projects.id` |
| SQL | Bahasa untuk memberi perintah ke database | `SELECT`, `INSERT` |
| CRUD | Empat pekerjaan dasar pada data: Create, Read, Update, Delete | `INSERT`, `SELECT`, `UPDATE`, `DELETE` |

### Kalau kamu tertinggal

Kamu tidak perlu menunggu atau memanggil trainer untuk hal yang bisa dikejar sendiri. Buka **Titik cek** terakhir yang berhasil kamu lewati, cocokkan hasilmu, lalu lanjut. Kalau sudah lebih dari satu bagian tertinggal, pakai **Jalur kejar** di bagian bawah.

---

## Bagian A — Persiapan (10 menit)

### A1 — Buka terminal Ubuntu

1. Tekan tombol Windows di keyboard.
2. Ketik kata `Ubuntu`.
3. Tekan Enter. Jendela hitam terbuka.

**Yang harus terlihat di baris terakhir (prompt):**

```text
nama@LAPTOP:~$
```

Kalau yang terlihat `PS C:\Users\...>`, itu PowerShell. Tutup, lalu buka lagi aplikasi **Ubuntu**.

### A2 — Nyalakan MySQL

**Folder:** bebas.

**Ketik di terminal:**

```text
sudo service mysql start
```

Kalau diminta password, itu password Ubuntu-mu (yang kamu buat waktu memasang Ubuntu). Hurufnya juga tidak tampil.

**Yang harus muncul di layar:** tulisan seperti `* Starting MySQL database server mysqld` atau tidak ada pesan error.

> Setiap kali laptop dihidupkan ulang atau Ubuntu ditutup lama, MySQL mati dan perintah ini harus diketik lagi.

### A3 — Cek login MySQL

**Folder:** bebas.

**Ketik di terminal** (ganti `p00` dengan ID-mu):

```text
mysql -u sakura_p00 -p sakura_db
```

Saat `Enter password:` muncul, ketik `sakura123` lalu Enter.

**Yang harus muncul di layar:** beberapa baris pembuka, lalu prompt:

```text
mysql>
```

Sekarang keluar lagi:

**Ketik di `mysql>`:**

```text
EXIT;
```

**Yang harus muncul di layar:** `Bye`, lalu kamu kembali ke terminal.

Kalau muncul `ERROR 2002`, MySQL belum menyala: ulangi A2. Kalau muncul `ERROR 1045`, user atau password salah: cek apakah `p00` sudah diganti ID-mu.

### A4 — Masuk ke repo materi

**Folder:** bebas.

**Ketik di terminal:**

```text
cd ~/seti-isd-materi
```

```text
git pull
```

**Yang harus muncul di layar:** `Already up to date.` atau daftar file yang diunduh. Kalau muncul `No such file or directory`, repo belum ada di laptop ini: panggil trainer.

### A5 — Buat folder kerjamu

Semua pekerjaanmu minggu ini disimpan di repo bersama `seti-isd-materi`, di dalam folder `minggu-03-database`. Tiap peserta punya folder sendiri bernama `sakura-tasks-` diikuti ID-mu, contoh `sakura-tasks-p00` atau `sakura-tasks-p01`. Jangan mengubah folder milik peserta lain.

**Folder:** `~/seti-isd-materi`

**Ketik di terminal** (ganti `p00` dengan ID-mu):

```text
mkdir -p minggu-03-database/sakura-tasks-p00/db
```

```text
cd minggu-03-database/sakura-tasks-p00
```

```text
pwd
```

**Yang harus muncul di layar** (nama di komputermu berbeda):

```text
/home/nama/seti-isd-materi/minggu-03-database/sakura-tasks-p00
```

### A6 — Buka folder di VS Code

**Folder:** `~/seti-isd-materi/minggu-03-database/sakura-tasks-p00`

**Ketik di terminal:**

```text
code .
```

**Yang harus muncul di layar:** jendela VS Code terbuka. Di pojok kiri bawah tertulis **WSL: Ubuntu**, dan panel kiri menampilkan folder `db`.

Buka terminal di dalam VS Code: tekan `Ctrl` dan tombol backtick (karakter di kiri angka 1). Mulai sekarang semua perintah di lembar ini diketik di terminal VS Code itu. Prompt-nya sudah berada di folder `sakura-tasks-p00`.

Kalau kamu membuka terminal baru, masuk lagi ke folder kerja dengan:

```text
cd ~/seti-isd-materi/minggu-03-database/sakura-tasks-p00
```

### Titik cek A

- [ ] `pwd` menampilkan alamat yang berakhir di `/minggu-03-database/sakura-tasks-p00`
- [ ] VS Code terbuka, tertulis **WSL: Ubuntu** di pojok kiri bawah
- [ ] Panel kiri VS Code menampilkan folder `db`
- [ ] Login ke MySQL pernah berhasil (A3)

---

## Bagian B — Membuat schema (20 menit)

Schema disimpan di file supaya bisa dijalankan ulang kapan saja.

### B1 — Buat file schema.sql

**Folder:** `sakura-tasks-p00`

**File:** `db/schema.sql` (baru)

Di panel kiri VS Code, klik kanan folder `db`, pilih **New File**, ketik `schema.sql`, lalu Enter.

**Isi file** (tempel, lalu simpan dengan `Ctrl+S`):

```sql
DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS projects;

CREATE TABLE projects (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  client VARCHAR(100) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tasks (
  id INT AUTO_INCREMENT PRIMARY KEY,
  project_id INT NOT NULL,
  title VARCHAR(150) NOT NULL,
  status ENUM('todo', 'doing', 'done') NOT NULL DEFAULT 'todo',
  priority TINYINT NOT NULL DEFAULT 2,
  due_date DATE NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (project_id) REFERENCES projects(id)
);
```

Dua tabel yang dibuat file ini: **projects** (daftar proyek) dan **tasks** (daftar tugas). Satu proyek punya banyak tugas.

### B2 — Jalankan schema.sql

**Folder:** `sakura-tasks-p00`

**Ketik di terminal** (ganti `p00` dengan ID-mu):

```text
mysql -u sakura_p00 -p sakura_db < db/schema.sql
```

Saat `Enter password:` muncul, ketik `sakura123` lalu Enter.

**Yang harus muncul di layar:** tidak ada tulisan apa-apa, prompt langsung kembali. Itu artinya berhasil. Kalau ada tulisan `ERROR`, baca pesannya, lalu lihat tabel "Masalah yang sering muncul" di bagian bawah.

### B3 — Periksa hasilnya

**Ketik di terminal:**

```text
mysql -u sakura_p00 -p sakura_db
```

**Ketik di `mysql>`:**

```text
SHOW TABLES;
```

**Yang harus muncul di layar:**

```text
+---------------------+
| Tables_in_sakura_db |
+---------------------+
| projects            |
| tasks               |
+---------------------+
2 rows in set
```

Kalau di `sakura_db` sudah ada tabel lain dari percobaanmu sebelumnya, tabel itu juga ikut tampil. Yang penting `projects` dan `tasks` ada.

**Ketik di `mysql>`:**

```text
DESCRIBE tasks;
```

**Yang harus muncul di layar:** tabel dengan 7 baris. Kolom pertamanya (`Field`) berisi: `id`, `project_id`, `title`, `status`, `priority`, `due_date`, `created_at`. Di bawahnya tertulis `7 rows in set`.

### B4 — Arti tipe data dan aturan kolom

Tabel ini dibaca saja. Trainer menjelaskan sambil menunjuk `schema.sql`.

| Tipe | Untuk apa |
| --- | --- |
| `INT` | Angka bulat |
| `TINYINT` | Angka bulat kecil (cukup untuk prioritas 1 sampai 3) |
| `VARCHAR(100)` | Teks pendek, maksimal 100 huruf |
| `ENUM('todo','doing','done')` | Hanya boleh salah satu dari tiga pilihan ini |
| `DATE` | Tanggal saja |
| `TIMESTAMP` | Tanggal dan jam |

| Aturan | Artinya |
| --- | --- |
| `PRIMARY KEY` | Nilainya tidak boleh kembar dan tidak boleh kosong |
| `AUTO_INCREMENT` | MySQL mengisi angka urut sendiri (1, 2, 3, ...) |
| `NOT NULL` | Tidak boleh kosong |
| `DEFAULT` | Nilai otomatis kalau tidak diisi |
| `FOREIGN KEY ... REFERENCES` | `project_id` harus berisi `id` proyek yang benar-benar ada |

### B5 — Coba melanggar aturan

Masih di dalam MySQL. Dua perintah ini **sengaja** dibuat salah, supaya kamu melihat aturan schema bekerja.

**Ketik di `mysql>`:**

```text
INSERT INTO tasks (project_id, title) VALUES (999, 'Coba coba');
```

**Yang harus muncul di layar:** error yang memuat `ERROR 1452` dan `Cannot add or update a child row: a foreign key constraint fails`.

**Ketik di `mysql>`:**

```text
INSERT INTO projects (name) VALUES ('Tanpa klien');
```

**Yang harus muncul di layar:** error yang memuat `ERROR 1364` dan `Field 'client' doesn't have a default value`.

Pertanyaan untukmu (jawab di kepala atau ke teman sebelahmu): kenapa keduanya ditolak? Aturan schema yang mana yang bekerja di tiap kasus?

### Titik cek B

- [ ] `SHOW TABLES;` menampilkan `projects` dan `tasks`
- [ ] `DESCRIBE tasks;` menampilkan 7 baris
- [ ] Dua perintah di B5 sama-sama ditolak, dengan nomor error `1452` dan `1364`

---

## Bagian C — Mengisi data awal (10 menit)

### C1 — Keluar dari MySQL

**Ketik di `mysql>`:**

```text
EXIT;
```

### C2 — Buat file seed.sql

**Folder:** `sakura-tasks-p00`

**File:** `db/seed.sql` (baru)

Di panel kiri VS Code, klik kanan folder `db`, pilih **New File**, ketik `seed.sql`, lalu Enter.

**Isi file** (tempel, lalu simpan dengan `Ctrl+S`):

```sql
INSERT INTO projects (name, client) VALUES
  ('Toko Online Kopi Nusantara', 'Kopi Nusantara'),
  ('Aplikasi Absensi Sekolah', 'SD Harapan'),
  ('Sistem Antrean Klinik', 'Klinik Sehat');

INSERT INTO tasks (project_id, title, status, priority, due_date) VALUES
  (1, 'Desain halaman produk', 'done', 1, '2026-11-10'),
  (1, 'Integrasi pembayaran', 'doing', 1, '2026-11-20'),
  (1, 'Fitur keranjang belanja', 'todo', 2, '2026-11-25'),
  (2, 'Halaman login guru', 'done', 2, '2026-11-12'),
  (2, 'Rekap absensi bulanan', 'todo', 2, '2026-11-30'),
  (2, 'Notifikasi orang tua', 'todo', 3, NULL),
  (3, 'Nomor antrean otomatis', 'doing', 1, '2026-11-22'),
  (3, 'Layar panggilan pasien', 'todo', 2, '2026-12-05');
```

### C3 — Jalankan seed.sql

**Ketik di terminal:**

```text
mysql -u sakura_p00 -p sakura_db < db/seed.sql
```

**Yang harus muncul di layar:** tidak ada tulisan apa-apa (artinya berhasil).

### C4 — Periksa isinya

**Ketik di terminal:**

```text
mysql -u sakura_p00 -p sakura_db
```

**Ketik di `mysql>`:**

```text
SELECT COUNT(*) FROM projects;
```

**Yang harus muncul di layar:**

```text
+----------+
| COUNT(*) |
+----------+
|        3 |
+----------+
```

**Ketik di `mysql>`:**

```text
SELECT COUNT(*) FROM tasks;
```

**Yang harus muncul di layar:** angka `8`.

### Titik cek C

- [ ] Proyek berjumlah 3
- [ ] Tugas berjumlah 8

---

## Bagian D — Melihat data dengan SELECT (20 menit)

Tetap di dalam MySQL. CRUD adalah empat pekerjaan dasar terhadap data, dan hampir semua aplikasi di dunia melakukan keempatnya:

| Huruf | Artinya | Perintah SQL |
| --- | --- | --- |
| C | Create (tambah data) | `INSERT` |
| R | Read (lihat data) | `SELECT` |
| U | Update (ubah data) | `UPDATE` |
| D | Delete (hapus data) | `DELETE` |

Bagian ini membahas huruf **R**. Ketik perintah satu per satu, lalu cocokkan hasilnya.

### D1 — Semua kolom, semua baris

**Ketik di `mysql>`:**

```text
SELECT * FROM tasks;
```

**Yang harus muncul di layar:** 8 baris, 7 kolom.

### D2 — Kolom tertentu

**Ketik di `mysql>`:**

```text
SELECT title, status FROM tasks;
```

**Yang harus muncul di layar:** 8 baris, hanya kolom `title` dan `status`.

### D3 — Filter dengan WHERE

**Ketik di `mysql>`:**

```text
SELECT title, due_date FROM tasks WHERE status = 'todo';
```

**Yang harus muncul di layar:** 4 baris: Fitur keranjang belanja (2026-11-25), Rekap absensi bulanan (2026-11-30), Notifikasi orang tua (`NULL`), dan Layar panggilan pasien (2026-12-05).

### D4 — Mengurutkan dengan ORDER BY

**Ketik di `mysql>`:**

```text
SELECT title, priority FROM tasks ORDER BY priority;
```

**Yang harus muncul di layar:** 8 baris. Tiga baris pertama berprioritas 1, dan baris terakhir (Notifikasi orang tua) berprioritas 3.

**Ketik di `mysql>`:**

```text
SELECT title, due_date FROM tasks ORDER BY due_date DESC;
```

**Yang harus muncul di layar:** 8 baris, tenggat terbaru di atas. Baris pertama: Layar panggilan pasien (2026-12-05). Baris yang `due_date`-nya `NULL` ada paling bawah.

### D5 — Membatasi jumlah baris dengan LIMIT

**Ketik di `mysql>`:**

```text
SELECT title, priority FROM tasks ORDER BY priority LIMIT 3;
```

**Yang harus muncul di layar:** 3 baris, ketiganya berprioritas 1.

### D6 — Dua syarat sekaligus dengan AND

**Ketik di `mysql>`:**

```text
SELECT title FROM tasks WHERE status = 'todo' AND priority = 2;
```

**Yang harus muncul di layar:** 3 baris: Fitur keranjang belanja, Rekap absensi bulanan, Layar panggilan pasien.

### D7 — Mencari potongan kata dengan LIKE

**Ketik di `mysql>`:**

```text
SELECT title FROM tasks WHERE title LIKE '%absensi%';
```

**Yang harus muncul di layar:** 1 baris: Rekap absensi bulanan. Tanda `%` artinya "huruf apa saja, berapa pun jumlahnya".

### D8 — Menghitung dengan COUNT

**Ketik di `mysql>`:**

```text
SELECT COUNT(*) FROM tasks WHERE status = 'done';
```

**Yang harus muncul di layar:** angka `2`.

### Titik cek D

- [ ] D3 menghasilkan 4 baris
- [ ] D6 menghasilkan 3 baris
- [ ] D7 menghasilkan 1 baris
- [ ] D8 menghasilkan angka 2

---

## Bagian E — Menambah, mengubah, menghapus (20 menit)

Tetap di dalam MySQL.

### E1 — Menambah proyek (INSERT)

**Ketik di `mysql>`:**

```text
INSERT INTO projects (name, client) VALUES ('Portal Karyawan', 'PT Maju Jaya');
```

**Yang harus muncul di layar:** `Query OK, 1 row affected`.

**Ketik di `mysql>`:**

```text
SELECT * FROM projects;
```

**Yang harus muncul di layar:** 4 baris. Proyek baru (`Portal Karyawan`) punya `id` 4 dan kolom `created_at` terisi tanggal dan jam hari ini. Kedua kolom itu kamu tidak isi, MySQL mengisinya sendiri.

### E2 — Menambah tugas untuk proyek baru

**Ketik di `mysql>`:**

```text
INSERT INTO tasks (project_id, title, priority) VALUES (4, 'Halaman slip gaji', 1);
```

**Ketik di `mysql>`:**

```text
SELECT * FROM tasks WHERE project_id = 4;
```

**Yang harus muncul di layar:** 1 baris. Kolom `status` berisi `todo` walaupun kamu tidak mengisinya. Itu kerja `DEFAULT`.

### E3 — Mengubah data (UPDATE)

**Ketik di `mysql>`:**

```text
UPDATE tasks SET status = 'doing' WHERE title = 'Halaman slip gaji';
```

**Yang harus muncul di layar:**

```text
Query OK, 1 row affected
Rows matched: 1  Changed: 1  Warnings: 0
```

`Rows matched` adalah jumlah baris yang cocok dengan `WHERE`. `Changed` adalah jumlah baris yang benar-benar berubah. Biasakan membaca keduanya setiap kali.

**Ketik di `mysql>`:**

```text
SELECT title, status FROM tasks WHERE project_id = 4;
```

**Yang harus muncul di layar:** `status` berisi `doing`.

Ubah dua kolom sekaligus:

**Ketik di `mysql>`:**

```text
UPDATE tasks SET status = 'done', priority = 3 WHERE title = 'Halaman slip gaji';
```

**Yang harus muncul di layar:** `Rows matched: 1  Changed: 1`.

### E4 — Menghapus data (DELETE)

**Ketik di `mysql>`:**

```text
DELETE FROM tasks WHERE title = 'Halaman slip gaji';
```

**Yang harus muncul di layar:** `Query OK, 1 row affected`.

**Ketik di `mysql>`:**

```text
SELECT COUNT(*) FROM tasks;
```

**Yang harus muncul di layar:** angka `8`.

### E5 — Aturan keselamatan: jangan lupa WHERE

Bagian ini dibaca saja. Di perusahaan, pernah ada developer yang ingin mengubah satu tugas, lupa menulis `WHERE`, dan seluruh status tugas di semua proyek berubah jadi `done`. Data lama tidak bisa kembali kalau tidak ada cadangan.

**Jangan diketik.** Dua perintah di bawah ini hanya untuk dibaca dan dipahami akibatnya:

```text
UPDATE tasks SET status = 'done';
DELETE FROM tasks;
```

Yang pertama mengubah **semua** baris di tabel `tasks`. Yang kedua menghapus **semua** baris di tabel `tasks`. Keduanya tidak punya `WHERE`.

Kebiasaan yang aman:

1. Tulis `SELECT ... WHERE ...` dulu untuk melihat baris mana yang akan kena.
2. Kalau barisnya sudah benar, ganti `SELECT ...` menjadi `UPDATE ...` atau `DELETE ...`, dengan `WHERE` yang sama.
3. Baca `Rows matched` atau `rows affected` setelahnya. Angkanya harus sama dengan yang kamu perkirakan.

### Titik cek E

- [ ] `SELECT * FROM projects;` menampilkan 4 baris (3 dari data awal, ditambah `Portal Karyawan`)
- [ ] `SELECT COUNT(*) FROM tasks;` menghasilkan `8`
- [ ] Kamu bisa menjelaskan ke teman: apa bedanya `UPDATE` dengan `WHERE` dan tanpa `WHERE`

---

## Bagian F — Misi 1 sampai 6 (25 menit)

Misi ini adalah **lanjutan Bagian A sampai E**. Kamu memakai database, tabel, dan data yang sama (`sakura_db`, tabel `projects` dan `tasks`, dengan keadaan data setelah Bagian E: 4 proyek dan 8 tugas). Semuanya dikerjakan di `mysql>`, belum memakai Python.

Mas Bayu menulis di grup tim, dan kamu mengerjakan permintaannya satu per satu. Kerjakan berurutan.

### F1 — Buat file latihan.sql

**Folder:** `sakura-tasks-p00`

**File:** `db/latihan.sql` (baru)

Di panel kiri VS Code, klik kanan folder `db`, pilih **New File**, ketik `latihan.sql`, lalu Enter.

**Semua perintah SQL yang kamu tulis untuk Misi 1 sampai 6, termasuk perintah `SELECT` untuk pengecekan, ditulis di file `db/latihan.sql`, urut sesuai nomor misi.** Tandai tiap misi dengan komentar, contoh:

```sql
-- Misi 1
INSERT INTO ...;
```

Kamu boleh mencoba perintahnya langsung di `mysql>` dulu, lalu menyalin yang benar ke file. Jangan lupa simpan file dengan `Ctrl+S`.

Contoh bentuk perintahnya ada di Bagian D dan E.

### Misi 1 — Menambah data

Mas Bayu: "Klien baru masuk. Tolong masukkan datanya ke database."

Kerjakan tiga langkah ini, berurutan:

1. Tambahkan **satu baris** ke tabel `projects`, dengan `name` berisi `Portal Alumni Kampus` dan `client` berisi `Kampus Merdeka`.
2. Lihat isi tabel `projects` dan catat nilai `id` milik `Portal Alumni Kampus`. Angka ini dipakai di langkah 3.
3. Tambahkan **dua baris** ke tabel `tasks`. Isi `project_id` dengan `id` dari langkah 2.
   - Baris pertama: `title` berisi `Desain halaman beranda`, `priority` berisi `1`.
   - Baris kedua: `title` berisi `Halaman daftar alumni`. Kolom `priority` tidak diisi, supaya memakai nilai bawaan.

Hasil yang benar:

- `SELECT COUNT(*) FROM tasks;` menghasilkan `10`.
- `SELECT title, priority FROM tasks WHERE project_id = ...;` (isi dengan `id` dari langkah 2) menghasilkan 2 baris: `Desain halaman beranda` dengan prioritas 1, dan `Halaman daftar alumni` dengan prioritas 2.

### Misi 2 — Menampilkan data dengan urutan

Mas Bayu: "Besok pagi saya mau lihat daftar tugas yang belum dikerjakan."

Tulis satu perintah `SELECT` dengan ketentuan ini:

1. Dari tabel `tasks`, tampilkan hanya kolom `title`, `priority`, dan `due_date`.
2. Tampilkan hanya baris yang kolom `status`-nya berisi `todo`.
3. Urutkan hasilnya berdasarkan `priority` dari angka kecil ke besar. Kalau `priority` sama, urutkan berdasarkan `due_date` dari tanggal terlama ke terbaru.

Hasil yang benar: 6 baris, dengan urutan:

1. Desain halaman beranda
2. Halaman daftar alumni
3. Fitur keranjang belanja
4. Rekap absensi bulanan
5. Layar panggilan pasien
6. Notifikasi orang tua

Baris yang `due_date`-nya kosong tampil sebagai `NULL`, dan di dalam kelompok `priority` yang sama baris itu ada paling atas.

### Misi 3 — Mengubah satu baris

Mas Bayu: "Tugas Integrasi pembayaran sudah selesai dikerjakan."

Kerjakan dua langkah ini:

1. Tulis perintah `UPDATE` pada tabel `tasks`: ubah kolom `status` menjadi `done` hanya pada baris yang kolom `title`-nya berisi `Integrasi pembayaran`.
2. Tulis perintah `SELECT` untuk menampilkan kolom `title` dan `status` dari baris tersebut.

Hasil yang benar:

- Setelah `UPDATE`, MySQL menampilkan `Rows matched: 1  Changed: 1`.
- Setelah `SELECT`, kolom `status` berisi `done`.

### Misi 4 — Menghapus satu baris

Mas Bayu: "Klien SD Harapan membatalkan fitur Notifikasi orang tua."

Kerjakan tiga langkah ini, berurutan:

1. Tulis perintah `SELECT COUNT(*)` pada tabel `tasks`, lalu catat angkanya. Angkanya harus `10`.
2. Tulis perintah `SELECT * FROM tasks` dengan `WHERE` kolom `title` berisi `Notifikasi orang tua`, untuk memastikan hanya 1 baris yang akan terhapus.
3. Tulis perintah `DELETE` pada tabel `tasks` dengan `WHERE` yang sama seperti langkah 2.

Hasil yang benar:

- Setelah `DELETE`, MySQL menampilkan `1 row affected`.
- Perintah `SELECT COUNT(*)` pada tabel `tasks` sekarang menghasilkan `9`.

### Misi 5 — Mengubah beberapa baris dengan satu perintah

Mas Bayu: "Klien SD Harapan minta semua tugas proyeknya dijadikan prioritas 1."

Proyek `Aplikasi Absensi Sekolah` (milik SD Harapan) punya `id` `2` di tabel `projects`. Kerjakan dua langkah ini:

1. Tulis perintah `SELECT` dengan kolom `title` dan `priority` dari tabel `tasks`, dengan `WHERE` kolom `project_id` berisi `2`. Pastikan hasilnya 2 baris.
2. Tulis **satu** perintah `UPDATE` pada tabel `tasks`: ubah kolom `priority` menjadi `1` pada semua baris yang `project_id`-nya `2`. Jangan menulis dua perintah `UPDATE` terpisah.

Hasil yang benar:

- Setelah `UPDATE`, MySQL menampilkan `Rows matched: 2  Changed: 2`.
- Kalau langkah 1 dijalankan lagi, kolom `priority` di kedua baris berisi `1`.

### Misi 6 — Menghapus baris yang masih dipakai tabel lain

Mas Bayu: "Proyek Toko Online Kopi Nusantara dibatalkan."

Kerjakan empat langkah ini, berurutan:

1. Tulis perintah `DELETE` pada tabel `projects` dengan `WHERE` kolom `name` berisi `Toko Online Kopi Nusantara`, lalu jalankan. Perintah ini akan menampilkan error. Itu memang yang diharapkan.
2. Di file `db/latihan.sql`, tulis sebagai komentar: nomor error dan satu kalimat jawaban untuk pertanyaan "Kenapa MySQL menolak perintah di langkah 1?"
3. Tulis perintah `DELETE` pada tabel `tasks` dengan `WHERE` kolom `project_id` berisi `1`, lalu jalankan.
4. Jalankan lagi perintah `DELETE` pada tabel `projects` dari langkah 1.

Hasil yang benar:

- Langkah 1 menampilkan `ERROR 1451` dengan pesan `Cannot delete or update a parent row`.
- Langkah 3 menampilkan `3 rows affected`.
- Langkah 4 menampilkan `1 row affected`.
- `SELECT COUNT(*) FROM projects;` menghasilkan `4`, dan `SELECT COUNT(*) FROM tasks;` menghasilkan `6`.

### Misi 7 — Bonus, kalau sempat

Mas Bayu: "Saya mau tahu jumlah tugas untuk tiap status."

Tulis satu perintah `SELECT` dengan ketentuan ini:

1. Dari tabel `tasks`, tampilkan kolom `status`, dan jumlah baris tiap status dengan nama kolom `jumlah` (pakai `COUNT(*) AS jumlah`).
2. Kelompokkan hasilnya per status dengan `GROUP BY status`.

Hasil yang benar (dengan data setelah Misi 6): 3 baris. `todo` berjumlah 4, `doing` berjumlah 1, `done` berjumlah 1.

### Titik cek F

- [ ] File `db/latihan.sql` berisi perintah jawaban Misi 1 sampai 6, ditandai komentar `-- Misi 1` dan seterusnya
- [ ] Nomor error dan jawaban satu kalimat dari Misi 6 tertulis sebagai komentar
- [ ] `SELECT COUNT(*) FROM projects;` menghasilkan `4` dan `SELECT COUNT(*) FROM tasks;` menghasilkan `6`
- [ ] Kamu bisa menjelaskan ke teman: kenapa Misi 6 langkah 1 ditolak dan langkah 4 berhasil

---

## Bagian G — Simpan ke Git dan GitHub (10 menit)

Keluar dari MySQL dulu kalau masih di dalamnya.

**Ketik di `mysql>`:**

```text
EXIT;
```

Pekerjaanmu disimpan ke repo bersama supaya trainer bisa melihatnya. Hanya folder milikmu yang disimpan.

### G1 — Masuk ke repo

**Ketik di terminal:**

```text
cd ~/seti-isd-materi
```

### G2 — Tandai folder milikmu

**Ketik di terminal** (ganti `p00` dengan ID-mu):

```text
git add minggu-03-database/sakura-tasks-p00
```

### G3 — Simpan sebagai commit

**Ketik di terminal:**

```text
git commit -m "Hari 1: schema, data awal, dan latihan CRUD"
```

**Yang harus muncul di layar:** tulisan seperti `3 files changed` (`schema.sql`, `seed.sql`, `latihan.sql`).

### G4 — Ambil pekerjaan teman, lalu kirim

Kalian semua menyimpan ke repo yang sama, jadi ambil dulu pekerjaan teman yang sudah lebih dulu dikirim:

**Ketik di terminal:**

```text
git pull --rebase
```

```text
git push
```

Kalau `git push` ditolak dengan tulisan `rejected` atau `fetch first`, ulangi dua perintah di atas, lalu coba lagi.

### G5 — Periksa di GitHub

Buka repo `seti-isd-materi` di GitHub lewat browser. Pastikan folder `minggu-03-database/sakura-tasks-p00/db` berisi `schema.sql`, `seed.sql`, dan `latihan.sql`.

### Titik cek G

- [ ] `git push` selesai tanpa error
- [ ] Tiga file ada di folder milikmu di GitHub

---

## Titik cek akhir Hari 1 dan jika ada masalah

### Target minimal Hari 1

- [ ] Tabel `projects` dan `tasks` ada di `sakura_db`
- [ ] Data awal ada (8 tugas sebelum Misi 1)
- [ ] File `schema.sql`, `seed.sql`, dan `latihan.sql` ada di folder `db` di dalam folder `sakura-tasks-p00` milikmu
- [ ] `latihan.sql` berisi perintah jawaban Misi 1 sampai 6, serta nomor error dan jawaban satu kalimat dari Misi 6
- [ ] Kamu bisa menjelaskan ke teman: apa beda `WHERE` dengan tanpa `WHERE` pada `UPDATE`
- [ ] Pekerjaanmu sudah di-push dan terlihat di GitHub

### Masalah yang sering muncul

| Pesan error | Penyebab | Yang dilakukan |
| --- | --- | --- |
| `ERROR 2002 Can't connect to local MySQL server` | MySQL belum menyala | `sudo service mysql start` |
| `ERROR 1045 Access denied` | Salah user atau password | Cek `p00` sudah diganti ID-mu dan password `sakura123` |
| `ERROR 1146 Table ... doesn't exist` | `schema.sql` belum dijalankan | Jalankan ulang perintah `mysql ... < db/schema.sql` |
| `ERROR 1062 Duplicate entry` | Data dengan nilai unik yang sama sudah ada | Baca bagian mana yang kembar di pesan error |
| `ERROR 1452 Cannot add or update a child row` | `project_id` yang diisi tidak ada di `projects` | Cek `SELECT * FROM projects;` |
| `ERROR 1451 Cannot delete or update a parent row` | Masih ada `tasks` yang menunjuk ke proyek itu | Ini yang dibahas di Misi 6 |
| `ERROR 1364 Field ... doesn't have a default value` | Kolom `NOT NULL` tanpa nilai bawaan tidak diisi | Isi kolom itu di `INSERT` |
| `ERROR 1064 You have an error in your SQL syntax` | Salah ketik (koma, kutip, titik koma) | Baca bagian yang disebut setelah `near`, periksa tanda baca |
| Prompt `->` muncul terus setelah Enter | Lupa titik koma `;` | Ketik `;` lalu Enter |
| `No such file or directory` saat `mysql ... < db/schema.sql` | Kamu tidak berada di folder `sakura-tasks-p00` | `cd ~/seti-isd-materi/minggu-03-database/sakura-tasks-p00`, lalu ulangi |
| `SELECT: command not found` | Perintah SQL diketik di terminal, padahal belum masuk MySQL | Masuk dulu dengan `mysql -u sakura_p00 -p sakura_db`, lalu ketik perintah SQL-nya |
| `ERROR 1064` saat mengetik `mysql -u ...` | Perintah terminal diketik di dalam MySQL | Ketik `EXIT;` dulu, lalu ketik perintahnya di terminal |
| `git push` ditolak (`rejected`, `fetch first`) | Teman sudah lebih dulu mengirim pekerjaan | `git pull --rebase`, lalu `git push` lagi |

Setelah mencoba sendiri dan bertanya ke AI atau mencari di internet masih macet? Tulis di grup.

### Jalur kejar

**Kalau tertinggal sampai sebelum Bagian D.** Pastikan `db/schema.sql` dan `db/seed.sql` sudah berisi teks dari B1 dan C2 (salin dari lembar ini). Jalankan keduanya dari folder `sakura-tasks-p00`:

```text
mysql -u sakura_p00 -p sakura_db < db/schema.sql
```

```text
mysql -u sakura_p00 -p sakura_db < db/seed.sql
```

Lanjutkan dari Bagian D.

**Kalau tertinggal sampai sebelum Bagian F (misi).** Setelah dua perintah di atas, masuk ke MySQL dan ketik satu perintah ini, supaya datamu sama dengan keadaan setelah Bagian E:

```text
INSERT INTO projects (name, client) VALUES ('Portal Karyawan', 'PT Maju Jaya');
```

`SELECT COUNT(*) FROM projects;` harus menghasilkan `4` dan `SELECT COUNT(*) FROM tasks;` harus `8`. Lanjutkan dari Bagian F.

**Kalau datamu berantakan dan ingin mengulang dari awal.** Jalankan lagi `schema.sql`, lalu `seed.sql`. Dua file itu mengembalikan semuanya ke keadaan awal (3 proyek, 8 tugas).

**Catatan.** Jangan mengubah `schema.sql` untuk menyelesaikan misi. Misi dikerjakan lewat perintah di `mysql>`.
