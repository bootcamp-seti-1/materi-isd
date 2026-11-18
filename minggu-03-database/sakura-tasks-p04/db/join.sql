-- soal 1

SELECT t.title , p.name , p.client
FROM tasks t 
JOIN projects p ON p.id = t.project_id
WHERE status = 'doing';

-- soal 2

SELECT t.title , p.name , t.due_date
FROM tasks t
JOIN projects p ON p.id = t.project_id
WHERE priority = 1 
ORDER BY t.due_date ASC;

--soal 3

SELECT 
    p.name,
    COUNT(t.id) AS jumlah_selesai
FROM 
    projects AS p 
LEFT JOIN tasks AS t
    ON p.id = t.project_id
    AND t.status = 'done'
GROUP BY p.id, p.name
ORDER BY p.id;
