SELECT p.name, COUNT(*) AS jumlah
FROM projects p
LEFT JOIN tasks t ON t.project_id = p.id AND t.status = 'done'
GROUP BY p.id, p.name;
