-- Misi 1
INSERT INTO projects (name, client) VALUES ('Portal Alumni Kampus', 'Kampus Merdeka');
SELECT * FROM projects;
INSERT INTO tasks (project_id, title, priority) VALUES (5, 'Desain halaman beranda', 1);
INSERT INTO tasks (project_id, title) VALUES (5, 'Halaman daftar alumni');
SELECT COUNT(*) FROM tasks;
SELECT title, priority FROM tasks WHERE project_id = 5;

-- Misi 2
SELECT title, priority, due_date FROM tasks WHERE status = 'todo' ORDER BY priority ASC, due_date ASC;

-- Misi 3
UPDATE tasks SET status = 'done' WHERE title = 'Integrasi pembayaran';
SELECT title, status FROM tasks WHERE title = 'Integrasi pembayaran';

-- Misi 4
SELECT COUNT(*) FROM tasks;
SELECT * FROM tasks WHERE title = 'Notifikasi orang tua';
DELETE FROM tasks WHERE title = 'Notifikasi orang tua';
SELECT COUNT(*) FROM tasks;

-- Misi 5
SELECT title, priority FROM tasks WHERE project_id = 2;
UPDATE tasks SET priority = 1 WHERE project_id = 2;
SELECT title, priority FROM tasks WHERE project_id = 2;

-- Misi 6
-- Perintah di bawah ini sengaja menghasilkan error:
-- DELETE FROM projects WHERE name = 'Toko Online Kopi Nusantara';
-- Nomor Error: ERROR 1451 (Cannot delete or update a parent row)
-- Jawaban: MySQL menolak penghapusan karena masih ada data tugas (child row) di tabel tasks yang terhubung ke proyek tersebut melalui Foreign Key.
DELETE FROM tasks WHERE project_id = 1;
DELETE FROM projects WHERE name = 'Toko Online Kopi Nusantara';
SELECT COUNT(*) FROM projects;
SELECT COUNT(*) FROM tasks;

-- Misi 7 (Bonus)
SELECT status, COUNT(*) AS jumlah FROM tasks GROUP BY status;
