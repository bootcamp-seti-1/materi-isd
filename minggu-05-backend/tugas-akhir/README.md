# Tugas Akhir Minggu 5 — Backend API

Ada dua sesi, masing-masing **60 menit**, dikerjakan di kelas.

| Sesi | Isi | Folder |
| --- | --- | --- |
| 1 | Kuis CTFd: 10 soal (4 easy, 3 medium, 3 hard) | `sesi-1-ctfd/` |
| 2 | Praktik: membuat API kantin sekolah dengan FastAPI dan MySQL | `sesi-2-kantin/` |

## Sesi 1 — Kuis CTFd

1. Buka terminal Ubuntu, lalu jalankan `sudo service mysql start`.
2. Nyalakan server soal (petunjuk lengkap di `sesi-1-ctfd/README.md`):

    ```text
    cd ~/seti-isd-materi/minggu-05-backend/tugas-akhir/sesi-1-ctfd/server-soal
    ```

    ```text
    uv run fastapi dev main.py --port 8100
    ```

3. Kerjakan soal per folder: `sesi-1-ctfd/soal-01` sampai `soal-10`. Buka `SOAL.md` di folder itu, baca ceritanya, lalu ikuti langkahnya.
4. Jawabannya teks pendek. Format jawaban ada di bagian "Cara menjawab" pada tiap soal.
5. Kirim jawabanmu ke CTFd: http://192.168.1.34:8000

Poin tiap soal: easy 100, medium 200, hard 300. Kamu tidak harus mengerjakan semuanya. Pilih soal sesuai poin yang ingin kamu kejar.

Aturan:
- Boleh membuka lembar Hari 1 dan Hari 2, kode `sakura-api` milikmu, dan bertanya ke trainer.
- Data server soal disimpan di memori. Kalau datanya berubah karena soal lain, restart server soal.

## Sesi 2 — Membuat API kantin sekolah

1. Ikuti petunjuk di `sesi-2-kantin/kantin-sekolah/README.md`. Di sana ada aturan API, data awal, dan cara mengembalikan data ke keadaan awal.
2. Kerjakan di kelas selama 60 menit.
3. Ada peringkat: skenario yang lulus paling banyak menang. Kalau jumlahnya sama, yang **waktu commit terakhirnya lebih awal** menang.
4. Kerjakan dan push di **branch milikmu sendiri** bernama `kantin-pXX` (contoh `kantin-p03`), bukan di `main`. Langkahnya ada di README sesi 2. Push sebelum batas waktu yang diumumkan trainer.
5. Hasilnya dibahas bersama di pertemuan berikutnya.

Aturan:
- Boleh memakai kode awal (template) yang disediakan dan kode `sakura-api` milikmu.
- Tidak ada alat cek otomatis. Periksa sendiri API-mu dengan `curl` atau `/docs`. Penilaian memakai banyak skenario yang tidak diperlihatkan, jadi coba kasus berhasil dan kasus yang harus ditolak.
- Kerjakan hanya di folder yang ada ID-mu. Folder `kantin-sekolah` tanpa ID adalah contoh asli, jangan diubah.
- Jangan mengubah `main.py`, `aturan.py`, `db.py`, dan folder `db`. File `.env` jangan di-push.
