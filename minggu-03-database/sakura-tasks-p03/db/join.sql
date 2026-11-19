-- Soal 1
SELECT t.title, p.name, p.client
FROM tasks t 
JOIN projects p 
ON t.project_id = p.id
WHERE t.status = 'doing';

-- Soal 2
SELECT t.title, p.name, t.due_date
FROM tasks t
JOIN projects p
ON t.project_id = p.id
WHERE t.priority = 1
ORDER BY due_date ASC;

-- Soal 3
SELECT p.name, COUNT(t.id) AS jumlah_selesai
FROM projects p
LEFT JOIN tasks t
ON p.id = t.project_id
AND t.status = 'done'
GROUP BY p.id, p.name
ORDER BY p.id;
