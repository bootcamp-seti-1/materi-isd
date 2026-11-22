DROP TABLE IF EXISTS members;

CREATE TABLE members (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

ALTER TABLE tasks ADD COLUMN member_id INT;
ALTER TABLE tasks ADD CONSTRAINT fk_tasks_member FOREIGN KEY (member_id) REFERENCES members(id);

INSERT INTO members (name) VALUES ('Budi'), ('Ani'), ('Siti');

UPDATE tasks SET member_id = 1 WHERE id IN (1, 2);
UPDATE tasks SET member_id = 2 WHERE id IN (3, 4);