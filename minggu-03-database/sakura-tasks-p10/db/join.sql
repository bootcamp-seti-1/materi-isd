-- SOAL 1
SELECT t.title, p.name, p.client AS proyek
 FROM tasks t
 JOIN projects p ON p.id = t.project_id
 WHERE status = "doing";

-- SOAL 2
SELECT t.title, p.name, t.due_date AS proyek
 FROM tasks t
 JOIN projects p ON p.id = t.project_id
 WHERE t.priority = 1
 ORDER BY t.due_date ASC;

-- SOAL 3
SELECT p.name, COUNT(t.id) AS jumlah_selesai
 FROM projects p
 LEFT JOIN tasks t ON p.id = t.project_id AND t.status = 'done'
 GROUP BY p.id, p.name  
 ORDER BY p.id;
