# Soal 10 — Absensi: dari Fungsi ke Class

**Tingkat:** Hard · **Poin:** 300
**Folder:** `~/latihan-python-h3/soal-10`

**Cerita.** Kantor Mas Bayu punya dua kelas pelatihan, A dan B. Dimas membuat program
absensi dengan gaya Hari 1: sekumpulan fungsi yang memakai satu catatan bersama. Begitu
dipakai untuk dua kelas sekaligus, datanya tercampur. Mas Bayu minta programnya diubah
ke gaya Hari 2: satu **class**, satu objek per kelas.

**Bahan.** Folder ini berisi `absensi.py` (versi prosedural milik Dimas, berisi fungsi
`hadir`, `izin`, `jumlah_hadir`, `jumlah_izin`, `rekap`) dan `demo.py` (kode pemakaian
yang sudah memakai class `Absensi`, **jangan diubah**). Saat ini `uv run demo.py` gagal
karena class `Absensi` belum ada.

**Tugasmu.** Ubah `absensi.py` menjadi class `Absensi`. Nama method sama dengan nama fungsi
sekarang (`hadir`, `izin`, `jumlah_hadir`, `jumlah_izin`, `rekap`), perilaku dan pesannya
tidak berubah, tapi setiap objek `Absensi` punya catatannya sendiri.

**Pertanyaan.** Setelah `demo.py` berjalan benar, dua baris `Hadir … | izin …` dicetak
untuk kelas A lalu kelas B. Apa empat angkanya?

**Cara menjawab.** Tulis empat angka sesuai urutan tercetak (hadir A, izin A, hadir B, izin B), dipisah koma tanpa spasi. Contoh bentuknya: `3,0,2,1`. Kirim jawabannya ke CTFd.
