# Tugas Akhir Minggu 3 — Database

Ada dua sesi, masing-masing **60 menit**, dikerjakan di kelas.

| Sesi | Isi | Folder |
| --- | --- | --- |
| 1 | Kuis CTFd: 10 soal (4 easy, 3 medium, 3 hard) | `sesi-1-ctfd/` |
| 2 | Praktik: membuat program koperasi sekolah dengan Python dan MySQL | `sesi-2-koperasi/` |

## Sesi 1 — Kuis CTFd

1. Buka terminal Ubuntu, lalu jalankan `sudo service mysql start`.
2. Kerjakan soal per folder: `sesi-1-ctfd/soal-01` sampai `soal-10`. Buka `SOAL.md` di folder itu, baca ceritanya, lalu ikuti langkah awalnya.
3. Jawabannya teks pendek. Format jawaban ada di bagian "Cara menjawab" pada tiap soal.
4. Kirim jawabanmu ke CTFd: http://192.168.1.34:8000

Poin tiap soal: easy 100, medium 200, hard 300. Kamu tidak harus mengerjakan semuanya. Pilih soal sesuai poin yang ingin kamu kejar. Panduan lengkap dan daftar soal ada di `sesi-1-ctfd/README.md`.

Aturan:
- Boleh membuka catatan Hari 1 sampai 3 dan bertanya ke trainer.
- Tiap soal berdiri sendiri. Jalankan `data.sql` di folder soal itu sebelum mulai, supaya datamu sama dengan peserta lain. Kalau data berubah, jalankan lagi.

## Sesi 2 — Membuat program koperasi sekolah

1. Ikuti petunjuk di `sesi-2-koperasi/koperasi-sekolah/README.md`. Di sana ada aturan program, contoh perintah, dan cara mengecek hasil kerjamu.
2. Kerjakan di kelas selama 60 menit.
3. Ada peringkat: skenario yang lulus paling banyak menang. Kalau jumlahnya sama, yang **waktu commit terakhirnya lebih awal** menang.
4. Push hasilmu ke GitHub **sebelum Minggu, 22 November 2026, pukul 23.59**.
5. Hasilnya dibahas bersama pada hari Senin.

Aturan:
- Boleh memakai kode awal (template) yang disediakan.
- Cek hasilmu dengan `cek.py`. Ada skenario lain yang tidak kamu lihat, jadi pikirkan juga kasus-kasus yang tidak ada di contoh.
- Kerjakan hanya di folder yang ada ID-mu. Folder `koperasi-sekolah` tanpa ID adalah contoh asli, jangan diubah.
- Jangan mengubah `main.py`, `aturan.py`, `db/schema.sql`, dan `db/seed.sql`. Satu-satunya perubahan di `db.py` adalah mengganti `sakura_p00` dengan ID-mu.
- Boleh commit dan push berkali-kali. Yang dihitung untuk peringkat adalah commit terakhir.
