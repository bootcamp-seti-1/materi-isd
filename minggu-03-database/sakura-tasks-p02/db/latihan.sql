-- !! Misi 1 — Menambah data
INSERT INTO projects (name, client) VALUES
    ('Portal Alumni Kampus', 'Kampus Merdeka')

INSERT INTO tasks (project_id, title, status, priority, due_date) VALUES
    (4, 'Desain halaman beranda', 'done', 1, '2026-11-10'),
    (4, 'Halaman daftar alumni', 'done', DEFAULT, '2026-11-10')

-- =======================================
-- Output (id: 4)
-- =======================================
-- | 10 |          4 | Desain halaman beranda  | done   |        1 | 2026-11-10 | 2026-11-17 09:40:21 |
-- | 11 |          4 | Halaman daftar alumni   | done   |        2 | 2026-11-10 | 2026-11-17 09:40:21 |
--
--
-- SELECT COUNT(*) FROM tasks;
-- +----------+
-- | count(*) |
-- +----------+
-- |       10 |
-- +----------+
-- 1 row in set (0.01 sec)
--
--
-- SELECT title, priority FROM tasks WHERE project_id = 4;
-- +------------------------+----------+
-- | title                  | priority |
-- +------------------------+----------+
-- | Desain halaman beranda |        1 |
-- | Halaman daftar alumni  |        2 |
-- +------------------------+----------+
-- 2 rows in set (0.01 sec)

-- !! Misi 2 — Menampilkan data dengan urutan
SELECT title, priority, due_date FROM tasks WHERE status = 'todo'
ORDER BY priority ASC, due_date ASC;

-- =======================================
-- Output
-- =======================================
-- SELECT title, priority, due_date FROM tasks WHERE status = 'todo' 
--     -> ORDER BY priority ASC, due_date ASC;
-- +-------------------------+----------+------------+
-- | title                   | priority | due_date   |
-- +-------------------------+----------+------------+
-- | Fitur keranjang belanja |        2 | 2026-11-25 |
-- | Rekap absensi bulanan   |        2 | 2026-11-30 |
-- | Layar panggilan pasien  |        2 | 2026-12-05 |
-- | Notifikasi orang tua    |        3 | NULL       |
-- +-------------------------+----------+------------+
-- 4 rows in set (0.04 sec)

-- !! Misi 3 — Mengubah satu baris
UPDATE tasks SET status = 'done' WHERE title = 'Integrasi pembayaran'
SELECT title, status FROM tasks WHERE title = 'Integrasi pembayaran'

-- =======================================
-- Output
-- =======================================
-- SELECT * FROM tasks;
-- +----+------------+-------------------------+--------+----------+------------+---------------------+
-- | id | project_id | title                   | status | priority | due_date   | created_at          |
-- +----+------------+-------------------------+--------+----------+------------+---------------------+
-- |  2 |          1 | Desain halaman produk   | done   |        1 | 2026-11-10 | 2026-11-17 09:02:51 |
-- |  3 |          1 | Integrasi pembayaran    | done   |        1 | 2026-11-20 | 2026-11-17 09:02:51 |
-- |  4 |          1 | Fitur keranjang belanja | todo   |        2 | 2026-11-25 | 2026-11-17 09:02:51 |
-- |  5 |          2 | Halaman login guru      | done   |        2 | 2026-11-12 | 2026-11-17 09:02:51 |
-- |  6 |          2 | Rekap absensi bulanan   | todo   |        2 | 2026-11-30 | 2026-11-17 09:02:51 |
-- |  7 |          2 | Notifikasi orang tua    | todo   |        3 | NULL       | 2026-11-17 09:02:51 |
-- |  8 |          3 | Nomor antrean otomatis  | doing  |        1 | 2026-11-22 | 2026-11-17 09:02:51 |
-- |  9 |          3 | Layar panggilan pasien  | todo   |        2 | 2026-12-05 | 2026-11-17 09:02:51 |
-- | 10 |          4 | Desain halaman beranda  | done   |        1 | 2026-11-10 | 2026-11-17 09:40:21 |
-- | 11 |          4 | Halaman daftar alumni   | done   |        2 | 2026-11-10 | 2026-11-17 09:40:21 |
-- +----+------------+-------------------------+--------+----------+------------+---------------------+
-- 10 rows in set (0.00 sec)
--
-- 
-- SELECT title, status FROM tasks WHERE title = 'Integrasi pembayaran'
-- +----------------------+--------+
-- | title                | status |
-- +----------------------+--------+
-- | Integrasi pembayaran | done   |
-- +----------------------+--------+
-- 1 row in set (0.08 sec)

-- !! Misi 4 — Menghapus satu baris
SELECT COUNT(*) FROM tasks;

SELECT * FROM tasks WHERE title = 'Notifikasi orang tua';

DELETE FROM tasks WHERE title = 'Notifikasi orang tua';

SELECT COUNT(*) FROM tasks;

-- =======================================
-- Output
-- =======================================
-- SELECT COUNT(*) FROM tasks;
-- +----------+
-- | COUNT(*) |
-- +----------+
-- |       10 |
-- +----------+
-- 1 row in set (0.18 sec)
--
--
-- SELECT * FROM tasks WHERE title = 'Notifikasi orang tua';
-- +----+------------+----------------------+--------+----------+----------+---------------------+
-- | id | project_id | title                | status | priority | due_date | created_at          |
-- +----+------------+----------------------+--------+----------+----------+---------------------+
-- |  7 |          2 | Notifikasi orang tua | todo   |        3 | NULL     | 2026-11-17 09:02:51 |
-- +----+------------+----------------------+--------+----------+----------+---------------------+
-- 1 row in set (0.02 sec)
-- 
--
-- DELETE FROM tasks WHERE title = 'Notifikasi orang tua';
-- Query OK, 1 row affected (0.12 sec)
-- 
--
-- SELECT COUNT(*) FROM tasks;
-- +----------+
-- | COUNT(*) |
-- +----------+
-- |        9 |
-- +----------+
-- 1 row in set (0.02 sec)

-- !! Misi 5 — Mengubah beberapa baris dengan satu perintah
SELECT title, priority FROM tasks WHERE project_id = 2;
UPDATE tasks SET priority = 1 WHERE project_id = 2;

-- =======================================
-- Output
-- =======================================
-- SELECT title, priority FROM tasks WHERE project_id = 2;
-- +-----------------------+----------+
-- | title                 | priority |
-- +-----------------------+----------+
-- | Halaman login guru    |        2 |
-- | Rekap absensi bulanan |        2 |
-- +-----------------------+----------+
-- 2 rows in set (0.02 sec)
--
--
-- UPDATE tasks SET priority = 1 WHERE project_id = 2;
-- Query OK, 2 rows affected (0.06 sec)
-- Rows matched: 2  Changed: 2  Warnings: 0

-- SELECT * FROM tasks;
-- +----+------------+-------------------------+--------+----------+------------+---------------------+
-- | id | project_id | title                   | status | priority | due_date   | created_at          |
-- +----+------------+-------------------------+--------+----------+------------+---------------------+
-- |  2 |          1 | Desain halaman produk   | done   |        1 | 2026-11-10 | 2026-11-17 09:02:51 |
-- |  3 |          1 | Integrasi pembayaran    | done   |        1 | 2026-11-20 | 2026-11-17 09:02:51 |
-- |  4 |          1 | Fitur keranjang belanja | todo   |        2 | 2026-11-25 | 2026-11-17 09:02:51 |
-- |  5 |          2 | Halaman login guru      | done   |        1 | 2026-11-12 | 2026-11-17 09:02:51 |
-- |  6 |          2 | Rekap absensi bulanan   | todo   |        1 | 2026-11-30 | 2026-11-17 09:02:51 |
-- |  8 |          3 | Nomor antrean otomatis  | doing  |        1 | 2026-11-22 | 2026-11-17 09:02:51 |
-- |  9 |          3 | Layar panggilan pasien  | todo   |        2 | 2026-12-05 | 2026-11-17 09:02:51 |
-- | 10 |          4 | Desain halaman beranda  | done   |        1 | 2026-11-10 | 2026-11-17 09:40:21 |
-- | 11 |          4 | Halaman daftar alumni   | done   |        2 | 2026-11-10 | 2026-11-17 09:40:21 |
-- +----+------------+-------------------------+--------+----------+------------+---------------------+
-- 9 rows in set (0.00 sec)

-- !! Misi 6 — Menghapus baris yang masih dipakai tabel lain
DELETE FROM projects WHERE name = 'Toko Online Kopi Nusantara';

DELETE FROM tasks WHERE project_id = 1;

DELETE FROM projects WHERE name = 'Toko Online Kopi Nusantara';

SELECT COUNT(*) FROM projects;
SELECT COUNT(*) FROM tasks;   

-- =======================================
-- Output
-- =======================================
-- DELETE FROM projects WHERE name = 'Toko Online Kopi Nusantara';
-- ERROR 1451 (23000): Cannot delete or update a parent row: a foreign key constraint fails (`sakura_db`.`tasks`, CONSTRAINT `tasks_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`))
-- Mengalami error saat pertama kali menghapus Toko Online Kopi Nusantara, ialah karena project Toko Online Kopi Nusantara masih dipakai oleh baris di tabel tasks (task-task itu memiliki project_id = 1). Sehingga perlu melakukan penghapusan terlebih dahulu data yang terhubung dengan Toko Online Kopi Nusantara yang ada di tabel tasks.
-- 
-- 
-- SELECT * FROM tasks;
-- +----+------------+------------------------+--------+----------+------------+---------------------+
-- | id | project_id | title                  | status | priority | due_date   | created_at          |
-- +----+------------+------------------------+--------+----------+------------+---------------------+
-- |  5 |          2 | Halaman login guru     | done   |        1 | 2026-11-12 | 2026-11-17 09:02:51 |
-- |  6 |          2 | Rekap absensi bulanan  | todo   |        1 | 2026-11-30 | 2026-11-17 09:02:51 |
-- |  8 |          3 | Nomor antrean otomatis | doing  |        1 | 2026-11-22 | 2026-11-17 09:02:51 |
-- |  9 |          3 | Layar panggilan pasien | todo   |        2 | 2026-12-05 | 2026-11-17 09:02:51 |
-- | 10 |          4 | Desain halaman beranda | done   |        1 | 2026-11-10 | 2026-11-17 09:40:21 |
-- | 11 |          4 | Halaman daftar alumni  | done   |        2 | 2026-11-10 | 2026-11-17 09:40:21 |
-- +----+------------+------------------------+--------+----------+------------+---------------------+
-- 6 rows in set (0.00 sec)
--
-- 
-- DELETE FROM projects WHERE name = 'Toko Online Kopi Nusantara';
-- Query OK, 1 row affected (0.10 sec)
--
-- SELECT COUNT(*) FROM projects;
-- +----------+
-- | COUNT(*) |
-- +----------+
-- |        3 |
-- +----------+
-- 1 row in set (0.04 sec) 
--
--
-- SELECT COUNT(*) FROM tasks; 
-- +----------+
-- | COUNT(*) |
-- +----------+
-- |        6 |
-- +----------+
-- 1 row in set (0.01 sec)
