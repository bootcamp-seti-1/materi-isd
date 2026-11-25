-- !! SOAL 1
-- Soal 1. Mas Bayu: "Tugas apa saja yang sedang dikerjakan?"
SELECT t.title, p.name, p.client FROM tasks t, projects p WHERE status = 'doing';

-- =======================================
-- Output
-- =======================================
-- SELECT t.title, p.name, p.client FROM tasks t, projects p WHERE status = 'doing';
-- +------------------------+--------------------------+----------------+
-- | title                  | name                     | client         |
-- +------------------------+--------------------------+----------------+
-- | Nomor antrean otomatis | Aplikasi Absensi Sekolah | SD Harapan     |
-- | Nomor antrean otomatis | Sistem Antrean Klinik    | Klinik Sehat   |
-- | Nomor antrean otomatis | Portal Alumni Kampus     | Kampus Merdeka |
-- +------------------------+--------------------------+----------------+
-- 3 rows in set (0.00 sec)

-- !! SOAL 2
-- Soal 2. Mas Bayu: "Saya mau lihat semua tugas prioritas 1, lengkap dengan nama proyeknya."
SELECT t.title, p.name, t.due_date 
FROM tasks t
JOIN projects p ON p.id = t.project_id
WHERE priority = 1
ORDER BY due_date DESC;

-- =======================================
-- Output
-- =======================================
-- SELECT t.title, p.name, t.due_date FROM tasks t JOIN projects p ON p.id = t.project_id WHERE priority = 1 ORDER BY due_date DESC;
-- +------------------------+--------------------------+------------+
-- | title                  | name                     | due_date   |
-- +------------------------+--------------------------+------------+
-- | Rekap absensi bulanan  | Aplikasi Absensi Sekolah | 2026-11-30 |
-- | Nomor antrean otomatis | Sistem Antrean Klinik    | 2026-11-22 |
-- | Halaman login guru     | Aplikasi Absensi Sekolah | 2026-11-12 |
-- | Desain halaman beranda | Portal Alumni Kampus     | 2026-11-10 |
-- +------------------------+--------------------------+------------+
-- 4 rows in set (0.04 sec)

-- !! SOAL 3
-- Soal 3. Mas Bayu: "Tiap proyek sudah menyelesaikan berapa tugas? Proyek yang belum menyelesaikan satu pun tetap harus muncul dengan angka 0."
SELECT p.name, COUNT(t.id) AS jumlah_selesai FROM projects p LEFT JOIN tasks t ON t.project_id = p.id WHERE t.status = 'done' GROUP BY p.id, p.name ORDER BY p.id;

-- =======================================
-- Output
-- =======================================
-- SELECT p.name, COUNT(t.id) AS jumlah_selesai FROM projects p LEFT JOIN tasks t ON t.project_id = p.id WHERE t.status = 'done' GROUP BY p.id, p.name ORDER BY p.id;
-- +--------------------------+----------------+
-- | name                     | jumlah_selesai |
-- +--------------------------+----------------+
-- | Aplikasi Absensi Sekolah |              1 |
-- | Portal Alumni Kampus     |              2 |
-- +--------------------------+----------------+
-- 2 rows in set (0.04 sec)