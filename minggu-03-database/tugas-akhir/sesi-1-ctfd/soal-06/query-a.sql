SELECT t.title, p.name
FROM tasks t
JOIN projects p ON p.id = t.project_id;
