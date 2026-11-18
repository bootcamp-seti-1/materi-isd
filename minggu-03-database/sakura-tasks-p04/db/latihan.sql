--  misi 1
--  1
INSERT INTO projects (name, client) VALUES
('Portal Alumni Kampus', 'Kampus Merdeka');

-- 2  
SELECT * FROM projects;

-- 3

INSERT INTO tasks (project_id, title, status, priority, due_date) VALUES
('4','Desain halaman beranda','todo','1','2026-12-12'),
('4','halaman daftar alumni','todo','1','2026-12-12');


-- Misi 2

SELECT title, priority, due_date FROM tasks WHERE status = 'todo' ORDER BY priority ASC ,due_date ASC;

-- Misi 3

UPDATE tasks 
SET status = 'done'
WHERE title = 'Itegrasi Pembayaran';

-- Misi 4

--1
SELECT COUNT(*) FROM tasks

--2
SELECT *
FROM tasks
WHERE title = 'Notifikasi orang tua';

--3
DELETE FROM tasks
WHERE title = 'Notifikasi orang tua';

-- Misi 5 

SELECT title, priority
FROM tasks
WHERE project_id = 2;

UPDATE tasks
SET priority = 1
WHERE project_id = 2;

-- Misi 6

DELETE FROM projects
WHERE name = 'Toko Online Kopi Nusantara';

-- ERROR 1451: MySQL menolak penghapusan karena proyek masih digunakan oleh tabel tasks melalui relasi Foreign Key (project_id).

DELETE FROM tasks
WHERE project_id = 1;

DELETE FROM projects
WHERE name = 'Toko Online Kopi Nusantara';

-- Misi 7

SELECT status, COUNT(*) AS jumlah
FROM tasks
GROUP BY status;