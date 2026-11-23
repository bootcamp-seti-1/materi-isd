-- Soal 4: tulis perintah SELECT-mu di bawah baris ini, diakhiri titik koma.
SELECT title, due_date
FROM tasks
WHERE status = 'todo' AND priority = 2
ORDER BY due_date ASC;
