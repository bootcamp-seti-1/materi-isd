# Sesi 2 — Program Parkir

Waktu: **60 menit**. Boleh memakai AI dan internet. Pahami kode yang kamu kumpulkan.

## Apa yang dibuat

Program yang mencatat kendaraan masuk dan keluar, lalu menampilkan biaya parkirnya.

```text
B1234AD masuk 18:23
B1234AD keluar 19:23
hasil
```

mencetak:

```text
B1234AD 1 jam tarif : 4000
```

Jalankan dengan `uv run main.py`. Program membaca input satu baris demi satu baris **tanpa mencetak
prompt apa pun**, dan berhenti saat input habis.

## Tiga perintah

| Perintah | Yang terjadi |
|---|---|
| `PLAT masuk JAM` | Kendaraan masuk. Tidak mencetak apa pun. |
| `PLAT keluar JAM` | Kendaraan keluar, biaya dihitung. Tidak mencetak apa pun. |
| `hasil` | Mencetak satu baris `PLAT N jam tarif : BIAYA` untuk tiap kendaraan yang **sudah keluar**. |

`JAM` selalu berbentuk `HH:MM` (24 jam). Semua kendaraan masuk dan keluar di hari yang sama.

## Aturan biaya

- Durasi dihitung dalam menit.
- **Gratis** kalau durasinya **15 menit atau kurang**.
- Selebihnya dibulatkan **ke atas per jam**: jam pertama **4000**, tiap jam berikutnya **2000**.
- Biaya **tidak pernah lebih dari 20000** per kendaraan.
- Contoh: 125 menit = 3 jam = 4000 + 2000 + 2000 = **8000**.
- Yang gratis tetap dicetak di `hasil` sebagai `A1 0 jam tarif : 0`.

## Aturan `hasil`

- Urutannya mengikuti siapa yang **keluar lebih dulu**.
- Kendaraan yang masih di dalam tidak ikut dicetak.
- Kalau belum ada yang keluar, tidak mencetak apa pun.
- `hasil` boleh dipanggil berkali-kali. Tiap panggilan mencetak semua yang sudah keluar sampai saat itu.
- Plat yang sama boleh masuk lagi setelah keluar. Parkirnya dihitung sebagai kendaraan baru.

## Pesan kesalahan

Pesan ini dicetak satu baris, dan keadaan parkir tidak berubah.

| Kejadian | Pesan |
|---|---|
| `masuk` untuk plat yang masih di dalam | `Plat sudah ada di dalam` |
| `keluar` untuk plat yang tidak ada di dalam | `Plat tidak ditemukan` |
| `keluar` dengan jam lebih awal dari jam masuk | `Jam keluar sebelum jam masuk` (kendaraan tetap di dalam) |

Plat ditulis apa adanya, tidak ada perubahan huruf besar atau kecil. Baris kosong diabaikan.

## Kerangka kode

Cari tulisan `TODO`.

| File | Keadaan | Tugasmu |
|---|---|---|
| `main.py` | sudah jadi | Jangan diubah. |
| `tarif.py` | angka tarif ada | Isi `Tarif.hitung`. |
| `parkir.py` | kerangka | Isi `masuk`, `keluar`, `hasil`. |

Angka tarif hanya boleh ada di `tarif.py`.

## Memeriksa pekerjaanmu

```text
uv run cek.py
```

`cek.py` menjalankan 6 contoh di folder `contoh/`. Penilaian memakai lebih banyak skenario, jadi buat
skenariomu sendiri.
