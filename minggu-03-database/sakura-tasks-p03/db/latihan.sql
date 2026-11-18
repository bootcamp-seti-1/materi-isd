-- Misi 1
INSERT INTO projects (name, client) VALUES
('Portal Alumni Kampus', 'Kampus Merdeka');

INSERT INTO tasks (project_id, title, priority) VALUES
(11, 'Desain halaman beranda', 1),
(11, 'Halaman daftar alumni', DEFAULT);

-- Misi 2
SELECT title, priority, due_date FROM tasks
WHERE status = 'todo'
ORDER BY priority ASC, due_date ASC;

-- Misi 3
UPDATE tasks SET status = 'done' WHERE title = 'Integrasi pembayaran';
SELECT title, status FROM tasks WHERE status = 'done';

-- Misi 4
SELECT * FROM tasks WHERE title = 'Notifikasi orang tua';
DELETE FROM tasks WHERE title = 'Notifikasi orang tua';

-- Misi 5
SELECT title, priority FROM tasks WHERE project_id = 2;
UPDATE tasks SET priority = 1 WHERE project_id = 2;

-- Misi 6
-- mysql> DELETE FROM projects WHERE name = 'Toko Online Kopi Nusantara';
-- ERROR 1451 (23000): Cannot delete or update a parent row: a foreign key constraint fails (`sakura_db`.`tasks`, CONSTRAINT `tasks_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`))
-- Kenapa MYSQL menolak perintah itu? gampangnya karena Toko Online Kopi Nusantara itu memiliki id yang digunakan di table tasks, jadi kalo itu dihapus tar title-title yg pake ID si Toko Online Kopi Nusantara mau punya relasi kemana? kan gak bisa makanya ditolak perintahnya
DELETE FROM tasks WHERE project_id = 1
DELETE FROM projects WHERE name = 'Toko Online Kopi Nusantara';

-- Misi 7 (Bonus)
SELECT status, COUNT(*) AS jumlah FROM tasks GROUP BY status;