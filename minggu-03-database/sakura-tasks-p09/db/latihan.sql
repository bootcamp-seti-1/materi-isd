-- misi 1
Tambahkan satu baris ke tabel projects, dengan name berisi Portal Alumni Kampus dan client berisi Kampus Merdeka.
mysql> INSERT INTO projects (name, client) VALUES ('Portal Alumni Kampus', 'Kampus Merdeka');
Query OK, 1 row affected (0.02 sec)

Lihat isi tabel projects dan catat nilai id milik Portal Alumni Kampus. Angka ini dipakai di langkah 3.
mysql> SELECT * FROM projects;
+----+----------------------------+----------------+---------------------+
| id | name                       | client         | created_at          |
+----+----------------------------+----------------+---------------------+
|  1 | Toko Online Kopi Nusantara | Kopi Nusantara | 2026-11-17 08:43:35 |
|  2 | Aplikasi Absensi Sekolah   | SD Harapan     | 2026-11-17 08:43:35 |
|  3 | Sistem Antrean Klinik      | Klinik Sehat   | 2026-11-17 08:43:35 |
|  4 | Portal Karyawan            | PT Maju Jaya   | 2026-11-17 08:58:04 |
|  5 | Portal Alumni Kampus       | Kampus Merdeka | 2026-11-17 09:07:58 |
+----+----------------------------+----------------+---------------------+
5 rows in set (0.00 sec)

Baris pertama: title berisi Desain halaman beranda, priority berisi 1.
mysql> INSERT INTO tasks (project_id, title, priority) VALUES (1, 'Desain Halaman Beranda', 1);
Query OK, 1 row affected (0.02 sec)

Baris kedua: title berisi Halaman daftar alumni. Kolom priority tidak diisi, supaya memakai nilai bawaan.
mysql> INSERT INTO tasks (project_id, title) VALUES (1, 'Halaman Daftar Alumni');
Query OK, 1 row affected (0.04 sec)

-- misi 2
Dari tabel tasks, tampilkan hanya kolom title, priority, dan due_date.
mysql> select title, priority, due_date from tasks;
+-------------------------+----------+------------+
| title                   | priority | due_date   |
+-------------------------+----------+------------+
| Desain halaman produk   |        1 | 2026-11-10 |
| Integrasi pembayaran    |        1 | 2026-11-20 |
| Fitur keranjang belanja |        2 | 2026-11-25 |
| Halaman login guru      |        2 | 2026-11-12 |
| Rekap absensi bulanan   |        2 | 2026-11-30 |
| Notifikasi orang tua    |        3 | NULL       |
| Nomor antrean otomatis  |        1 | 2026-11-22 |
| Layar panggilan pasien  |        2 | 2026-12-05 |
| Halaman slip gaji       |        3 | NULL       |
| Desain Halaman Beranda  |        1 | NULL       |
| Halaman Daftar Alumni   |        2 | NULL       |
+-------------------------+----------+------------+
11 rows in set (0.00 sec)

Tampilkan hanya baris yang kolom status-nya berisi todo.
mysql> select title from tasks where status = 'todo';
+-------------------------+
| title                   |
+-------------------------+
| Fitur keranjang belanja |
| Rekap absensi bulanan   |
| Notifikasi orang tua    |
| Layar panggilan pasien  |
| Desain Halaman Beranda  |
| Halaman Daftar Alumni   |
+-------------------------+
6 rows in set (0.00 sec)

Urutkan hasilnya berdasarkan priority dari angka kecil ke besar. Kalau priority sama, urutkan berdasarkan due_date dari tanggal terlama ke terbaru.
mysql> select title, priority, due_date from tasks order by priority asc, due_date asc;
+-------------------------+----------+------------+
| title                   | priority | due_date   |
+-------------------------+----------+------------+
| Desain Halaman Beranda  |        1 | NULL       |
| Desain halaman produk   |        1 | 2026-11-10 |
| Integrasi pembayaran    |        1 | 2026-11-20 |
| Nomor antrean otomatis  |        1 | 2026-11-22 |
| Halaman Daftar Alumni   |        2 | NULL       |
| Halaman login guru      |        2 | 2026-11-12 |
| Fitur keranjang belanja |        2 | 2026-11-25 |
| Rekap absensi bulanan   |        2 | 2026-11-30 |
| Layar panggilan pasien  |        2 | 2026-12-05 |
| Notifikasi orang tua    |        3 | NULL       |
| Halaman slip gaji       |        3 | NULL       |
+-------------------------+----------+------------+
11 rows in set (0.00 sec)

-- misi 3
Tulis perintah UPDATE pada tabel tasks: ubah kolom status menjadi done hanya pada baris yang kolom title-nya berisi Integrasi pembayaran.
mysql> update tasks set status = 'done' where title = 'Integrasi pembayaran';
Query OK, 1 row affected (0.03 sec)
Rows matched: 1  Changed: 1  Warnings: 0

Tulis perintah SELECT untuk menampilkan kolom title dan status dari baris tersebut.
mysql> SELECT title, status FROM tasks WHERE title LIKE '%Integrasi%';
+----------------------+--------+
| title                | status |
+----------------------+--------+
| Integrasi pembayaran | done   |
+----------------------+--------+
1 row in set (0.00 sec)

-- misi 4
Tulis perintah SELECT COUNT(*) pada tabel tasks, lalu catat angkanya. Angkanya harus 10.
mysql> select * from tasks;
+----+------------+-------------------------+--------+----------+------------+---------------------+
| id | project_id | title                   | status | priority | due_date   | created_at          |
+----+------------+-------------------------+--------+----------+------------+---------------------+
|  2 |          1 | Desain halaman produk   | done   |        1 | 2026-11-10 | 2026-11-17 08:43:35 |
|  3 |          1 | Integrasi pembayaran    | done   |        1 | 2026-11-20 | 2026-11-17 08:43:35 |
|  4 |          1 | Fitur keranjang belanja | todo   |        2 | 2026-11-25 | 2026-11-17 08:43:35 |
|  5 |          2 | Halaman login guru      | done   |        2 | 2026-11-12 | 2026-11-17 08:43:35 |
|  6 |          2 | Rekap absensi bulanan   | todo   |        2 | 2026-11-30 | 2026-11-17 08:43:35 |
|  7 |          2 | Notifikasi orang tua    | todo   |        3 | NULL       | 2026-11-17 08:43:35 |
|  8 |          3 | Nomor antrean otomatis  | doing  |        1 | 2026-11-22 | 2026-11-17 08:43:35 |
|  9 |          3 | Layar panggilan pasien  | todo   |        2 | 2026-12-05 | 2026-11-17 08:43:35 |
| 11 |          1 | Desain Halaman Beranda  | todo   |        1 | NULL       | 2026-11-17 09:13:31 |
| 12 |          1 | Halaman Daftar Alumni   | todo   |        2 | NULL       | 2026-11-17 09:14:11 |
+----+------------+-------------------------+--------+----------+------------+---------------------+
10 rows in set (0.00 sec)

Tulis perintah SELECT * FROM tasks dengan WHERE kolom title berisi Notifikasi orang tua, untuk memastikan hanya 1 baris yang akan terhapus.
mysql> SELECT title, status FROM tasks WHERE title LIKE '%Notifikasi%';
+----------------------+--------+
| title                | status |
+----------------------+--------+
| Notifikasi orang tua | todo   |
+----------------------+--------+
1 row in set (0.00 sec)

Tulis perintah DELETE pada tabel tasks dengan WHERE yang sama seperti langkah 2.
mysql> SELECT title, status FROM tasks WHERE title LIKE '%Notifikasi%';
Empty set (0.00 sec) 

-- misi 5
Tulis perintah SELECT dengan kolom title dan priority dari tabel tasks, dengan WHERE kolom project_id berisi 2. Pastikan hasilnya 2 baris.
mysql> select title, priority from tasks where project_id = 2;
+-----------------------+----------+
| title                 | priority |
+-----------------------+----------+
| Halaman login guru    |        2 |
| Rekap absensi bulanan |        2 |
+-----------------------+----------+
2 rows in set (0.00 sec)

Tulis satu perintah UPDATE pada tabel tasks: ubah kolom priority menjadi 1 pada semua baris yang project_id-nya 2. Jangan menulis dua perintah UPDATE terpisah.
mysql> update tasks set priority = 1 where project_id = 2;
Query OK, 2 rows affected (0.04 sec)
Rows matched: 2  Changed: 2  Warnings: 0

-- misi 6
Tulis perintah DELETE pada tabel projects dengan WHERE kolom name berisi Toko Online Kopi Nusantara, lalu jalankan. Perintah ini akan menampilkan error. Itu memang yang diharapkan.
mysql> DELETE FROM projects WHERE name = 'Toko Online Kopi Nusantara';
ERROR 1451 (23000): Cannot delete or update a parent row: a foreign key constraint fails (`sakura_db`.`tasks`, CONSTRAINT `tasks_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`))

Di file db/latihan.sql, tulis sebagai komentar: nomor error dan satu kalimat jawaban untuk pertanyaan "Kenapa MySQL menolak perintah di langkah 1?"


Tulis perintah DELETE pada tabel tasks dengan WHERE kolom project_id berisi 1, lalu jalankan.
mysql> DELETE FROM tasks WHERE project_id = '1';
Query OK, 5 rows affected (0.01 sec)

Jalankan lagi perintah DELETE pada tabel projects dari langkah 1.
mysql> DELETE FROM projects WHERE name = 'Toko Online Kopi Nusantara';
Query OK, 1 row affected (0.05 sec)

-- misi 7
Dari tabel tasks, tampilkan kolom status, dan jumlah baris tiap status dengan nama kolom jumlah (pakai COUNT(*) AS jumlah).
mysql> SELECT status from tasks;
+--------+
| status |
+--------+
| done   |
| todo   |
| doing  |
| todo   |
+--------+
4 rows in set (0.01 sec)

mysql> SELECT COUNT(*) AS jumlah from tasks;
+--------+
| jumlah |
+--------+
|      4 |
+--------+
1 row in set (0.00 sec)

Kelompokkan hasilnya per status dengan GROUP BY status.
mysql> SELECT status, COUNT(*) AS jumlah from tasks group by status;
+--------+--------+
| status | jumlah |
+--------+--------+
| done   |      1 |
| todo   |      2 |
| doing  |      1 |
+--------+--------+
3 rows in set (0.03 sec)
