-- Data awal Sakura Tasks. Isinya sama dengan schema.sql dan seed.sql dari Hari 1.
-- Menjalankan file ini mengembalikan tabel projects dan tasks ke keadaan awal: 3 proyek dan 8 tugas.
DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS projects;

CREATE TABLE projects (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  client VARCHAR(100) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tasks (
  id INT AUTO_INCREMENT PRIMARY KEY,
  project_id INT NOT NULL,
  title VARCHAR(150) NOT NULL,
  status ENUM('todo', 'doing', 'done') NOT NULL DEFAULT 'todo',
  priority TINYINT NOT NULL DEFAULT 2,
  due_date DATE NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (project_id) REFERENCES projects(id)
);

INSERT INTO projects (name, client) VALUES
  ('Toko Online Kopi Nusantara', 'Kopi Nusantara'),
  ('Aplikasi Absensi Sekolah', 'SD Harapan'),
  ('Sistem Antrean Klinik', 'Klinik Sehat');

INSERT INTO tasks (project_id, title, status, priority, due_date) VALUES
  (1, 'Desain halaman produk', 'done', 1, '2026-11-10'),
  (1, 'Integrasi pembayaran', 'doing', 1, '2026-11-20'),
  (1, 'Fitur keranjang belanja', 'todo', 2, '2026-11-25'),
  (2, 'Halaman login guru', 'done', 2, '2026-11-12'),
  (2, 'Rekap absensi bulanan', 'todo', 2, '2026-11-30'),
  (2, 'Notifikasi orang tua', 'todo', 3, NULL),
  (3, 'Nomor antrean otomatis', 'doing', 1, '2026-11-22'),
  (3, 'Layar panggilan pasien', 'todo', 2, '2026-12-05');
