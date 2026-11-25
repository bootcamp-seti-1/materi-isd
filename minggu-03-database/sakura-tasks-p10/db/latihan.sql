-- MISI 1
INSERT INTO projects (name, client)
VALUES ("Portal Alumni Kampus", "Kampus Merdeka");

INSERT INTO tasks (project_id, title, priority) VALUES 
(5, "Desain halaman beranda", 1),
(5, "Halaman daftar alumni", DEFAULT);

-- MISI 2

SELECT title, priority, due_date FROM tasks
 WHERE status="todo"
 ORDER BY priority ASC, (due_date IS NULL) DESC, due_date DESC;

-- MISI 3
UPDATE tasks
 SET status = "done"
 WHERE title = "Integrasi pembayaran";

-- MISI 4

-- Check
SELECT COUNT(*) from tasks;  -- 10
SELECT * FROM tasks WHERE title = "Notifikasi orang tua";

-- Delete that one
DELETE FROM tasks WHERE title = "Notifikasi orang tua";

-- Check again
SELECT COUNT(*) from tasks;  -- 9

-- Misi 5

-- Check
SELECT title, priority
 FROM tasks 
 WHERE project_id = 2;

-- Update
UPDATE tasks 
 SET priority = 1
 WHERE project_id = 2;

-- Misi 6

DELETE FROM projects WHERE name = "Toko Online Kopi Nusantara";
-- Cannot delete because of foreign Key Constraint (`sakura_db`.`tasks`, CONSTRAINT `tasks_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`))
-- Rules where delete denied when there are tasks that still have foreign key from the deleted project.

-- Delete the linked tasks first.
DELETE FROM tasks WHERE project_id = 1;
-- Then delete the project.
DELETE FROM projects WHERE name = "Toko Online Kopi Nusantara";

-- Misi 7

SELECT status, COUNT(*) AS jumlah
FROM tasks
GROUP BY status;