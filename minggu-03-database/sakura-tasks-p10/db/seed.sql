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