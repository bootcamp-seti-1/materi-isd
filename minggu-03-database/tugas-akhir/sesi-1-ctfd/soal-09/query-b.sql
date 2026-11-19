SELECT p.name, COUNT(t.id) AS jumlah
FROM projects p
LEFT JOIN tasks t ON t.project_id = p.id
WHERE t.status = 'done'
GROUP BY p.id, p.name;
