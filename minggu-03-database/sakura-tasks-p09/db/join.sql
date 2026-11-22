-- soal 1
Dari tabel tasks (alias t), JOIN dengan tabel projects (alias p).
Tampilkan kolom t.title, p.name, dan p.client.
Tampilkan hanya baris yang status-nya doing.
mysql> SELECT t.title, p.name, p.client
    -> from tasks t
    -> JOIN projects p ON p.id = t.project_id
    -> where t.status = 'doing'
    -> order by t.due_date;
+------------------------+-----------------------+--------------+
| title                  | name                  | client       |
+------------------------+-----------------------+--------------+
| Nomor antrean otomatis | Sistem Antrean Klinik | Klinik Sehat |
+------------------------+-----------------------+--------------+
1 row in set (0.00 sec)

-- soal 2
Dari tabel tasks (alias t), JOIN dengan tabel projects (alias p).
Tampilkan kolom t.title, p.name, dan t.due_date.
Tampilkan hanya baris yang priority-nya 1.
Urutkan berdasarkan t.due_date dari tanggal terlama ke terbaru.
mysql> select t.title, p.name, t.due_date
    -> from tasks t
    -> JOIN projects p ON p.id = t.project_id
    -> where t.priority = '1' 
    -> order by t.due_date;
+------------------------+--------------------------+------------+
| title                  | name                     | due_date   |
+------------------------+--------------------------+------------+
| Halaman login guru     | Aplikasi Absensi Sekolah | 2026-11-12 |
| Nomor antrean otomatis | Sistem Antrean Klinik    | 2026-11-22 |
| Rekap absensi bulanan  | Aplikasi Absensi Sekolah | 2026-11-30 |
+------------------------+--------------------------+------------+
3 rows in set (0.00 sec)

-- soal 3
Dari tabel projects (alias p), LEFT JOIN dengan tabel tasks (alias t).
Tampilkan p.name dan jumlah tugas selesai dengan nama kolom jumlah_selesai.
Kelompokkan dengan GROUP BY p.id, p.name, dan urutkan dengan ORDER BY p.id.
mysql> select p.name, count(t.id) AS jumlah_tugas 
    -> from projects p
    -> left join tasks t on t.project_id = p.id
    -> group by p.id, p.name
    -> order by p.id;
+--------------------------+--------------+
| name                     | jumlah_tugas |
+--------------------------+--------------+
| Aplikasi Absensi Sekolah |            2 |
| Sistem Antrean Klinik    |            2 |
| Portal Karyawan          |            0 |
| Portal Alumni Kampus     |            0 |
+--------------------------+--------------+
4 rows in set (0.00 sec) 