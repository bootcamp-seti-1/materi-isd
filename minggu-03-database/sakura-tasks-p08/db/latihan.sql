-- Misi 1
-- tambah satu baris
INSERT INTO projects (name, client) VALUES ('Portal Alumni Kampus', 'Kampus Merdeka');
-- lihat isi
SELECT id, name FROM projects WHERE name = 'Portal Alumni Kampus';
-- tambah dua baris
INSERT INTO tasks (title, priority, status, project_id) VALUES
('Desain halaman beranda', '1', 'done', 7),
('Halaman daftar alumni', '1', 'done', 7);

-- misi 2
-- no 1
SELECT title, priority, due_date FROM tasks;
-- no 2
SELECT * FROM tasks WHERE status = 'todo';
-- no 3
SELECT * FROM tasks ORDER BY priority asc, due_date asc;

-- misi 3
-- no 1
UPDATE tasks SET status = 'done' WHERE title = 'Integrasi pembayaran';
SELECT title, status FROM tasks WHERE title = 'Integrasi pembayaran';

-- misi 4
-- no 1
SELECT COUNT(*) FROM tasks;
-- no 2
SELECT * FROM tasks WHERE title = 'Notifikasi orang tua';
-- no 3
DELETE FROM tasks WHERE title = 'Notifikasi orang tua';

-- misi 5
-- no 1
SELECT title, priority FROM tasks WHERE project_id = 2;
-- no 2
UPDATE tasks SET priority = 1 WHERE project_id = 2;

-- misi 6
-- no 1
DELETE FROM projects WHERE name = 'Toko Online Kopi Nusantara';
-- no 2
'ERROR 1451 (23000): Cannot delete or update a parent row: a foreign key constraint fails (`sakura_db`.`tasks`, CONSTRAINT `tasks_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`))'

'penyebabnya adalah fk pada tabel tasks yang diambil dari id pada tabel projects masih ada yang mengacu pada project_id dengan value 1 (Toko Online Kopi Nusantara), sehingga tidak bisa dihapus. maka harus dihapus terlebih dahulu data fk project_id value 1 pada tabel tasks, baru bisa menghapus data project_id value 1 pada tabel projects'

-- no 3
DELETE FROM tasks WHERE project_id = 1;

-- no 4
DELETE FROM projects WHERE name = 'Toko Online Kopi Nusantara';

-- misi 7
-- no 1
mysql> SELECT status, COUNT(*) AS jumlah FROM tasks GROUP BY status;
+--------+--------+
| status | jumlah |
+--------+--------+
| done   |      3 |
| todo   |      2 |
| doing  |      1 |
+--------+--------+
3 rows in set (0.01 sec)