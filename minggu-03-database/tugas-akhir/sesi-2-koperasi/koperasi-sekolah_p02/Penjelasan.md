# Panduan Memahami Tugas Koperasi Sekolah

Dokumen ini menjelaskan tujuan tugas, hubungan antarfile, alur program, isi penting `koperasi.py`, dan langkah mengerjakan fungsi-fungsi yang masih kosong. Penjelasannya mengikuti file yang ada di folder proyek ini.

## 1. Tujuan tugas

Bu Ratna mengelola koperasi sekolah dan ingin mengganti pencatatan manual dengan program yang menyimpan data di MySQL. Program menerima perintah seperti:

```text
isi Andi 5000
saldo Andi
beli Andi Pensil 2
laporan
stok
batal 1
```

Setiap baris adalah satu perintah. Program memproses baris-baris itu sampai input habis. Data saldo, barang, dan pembelian disimpan di database, jadi fungsi program bukan sekadar menghitung lalu membuang hasilnya.

Hal yang dinilai bukan hanya apakah perintah berhasil, tetapi juga:

- pesan kesalahan harus tepat;
- pemeriksaan harus dilakukan dalam urutan yang ditentukan;
- kegagalan tidak boleh mengubah data;
- angka dan urutan keluaran harus sesuai format;
- pembelian yang dibatalkan tidak boleh masuk laporan atau hitungan batas pembelian.

README menyebut waktu pengerjaan 60 menit, memperbolehkan penggunaan AI dan internet, dan mengingatkan agar peserta memahami kode karena trainer dapat menanyakannya. Hasil akhir harus di-push ke GitHub sesuai tenggat yang tercantum di README. Penilaian menggunakan lebih banyak skenario daripada contoh yang disediakan.

## 2. Peta program: siapa melakukan apa?

Alur sederhananya seperti ini:

```text
Baris perintah
    ↓
main.py membaca dan mengenali bentuk perintah
    ↓
koperasi.py menjalankan aturan dan memilih pesan/hasil
    ↓
db.py membaca atau mengubah data di MySQL
    ↓
Tabel students, items, dan purchases
```

### `main.py`: penerima dan pengarah perintah

[`main.py`](./main.py) membuat satu objek `Koperasi`, lalu membaca input berulang kali. Setiap baris dipecah dengan `split()`, sehingga kata-kata di baris menjadi bagian-bagian perintah.

Contohnya:

```text
beli Andi Pensil 2
```

dipecah menjadi empat bagian: `beli`, `Andi`, `Pensil`, `2`. Karena jumlah bagian dan kata pertama cocok, `main.py` memanggil fungsi `koperasi.beli("Andi", "Pensil", "2")`.

Penting: nilai seperti `2` masih diberikan sebagai teks. Fungsi yang menerima jumlah atau nominal perlu memvalidasinya dan mengubahnya menjadi bilangan bulat.

`main.py` hanya mengatur rute perintah; aturan bisnisnya berada di `koperasi.py`. Jangan menambahkan prompt seperti `Masukkan perintah:` karena program harus membaca input tanpa mencetak prompt. Ketika input habis, `input()` menghasilkan `EOFError` dan perulangan berhenti.

Perintah yang dikenali:

| Bentuk input | Fungsi yang dipanggil |
|---|---|
| `isi NAMA NOMINAL` | `isi(nama, nominal)` |
| `saldo NAMA` | `saldo(nama)` |
| `beli NAMA BARANG JUMLAH` | `beli(nama, barang, jumlah)` |
| `laporan` | `laporan()` |
| `stok` | `stok()` |
| `batal NOMOR` | `batal(nomor)` |

Baris kosong dan bentuk perintah yang tidak cocok tidak masuk ke cabang mana pun, sehingga diabaikan. Karena `split()` memisah berdasarkan spasi, README menetapkan nama barang tidak memakai spasi, misalnya `Buku_Tulis`.

### `koperasi.py`: aturan koperasi

[`koperasi.py`](./koperasi.py) adalah file utama yang dikerjakan. Kelas `Koperasi` berisi enam fungsi yang sesuai dengan enam perintah. Fungsi-fungsi ini bertugas:

1. meminta data dari database;
2. mengecek input dan kondisi sesuai urutan aturan;
3. mencetak pesan atau laporan jika diperlukan;
4. menyimpan perubahan jika operasi berhasil.

Fungsi yang berhasil seperti `isi` dan `beli` tidak mencetak pesan sukses. Pesan hanya dicetak bila aturan meminta pesan tertentu atau bila perintah memang berupa laporan/saldo/stok.

### `db.py`: penghubung ke MySQL

[`db.py`](./db.py) memiliki dua fungsi yang dipakai `koperasi.py`:

- `fetch_all(sql, params)` menjalankan query baca dan mengembalikan baris sebagai daftar dictionary. Misalnya satu baris dapat diakses melalui `baris["id"]` atau `baris["balance"]`.
- `execute(sql, params)` menjalankan query perubahan seperti `UPDATE` atau `INSERT`, lalu melakukan `commit`.

Parameter query ditulis dengan placeholder `%s`, lalu nilainya dikirim terpisah sebagai tuple. Contoh yang sudah ada:

```python
fetch_all(
    "SELECT id FROM students WHERE BINARY name = %s",
    (nama,)
)
```

Cara ini membuat nilai input tidak perlu ditempel langsung ke teks SQL.

`db.py` juga mengatur alamat database, nama pengguna, password, dan nama database. README meminta nama pengguna disesuaikan dengan ID peserta. Pada salinan proyek ini, konfigurasi pengguna sudah tertulis `sakura_p02`; pastikan itu memang ID yang ditentukan untukmu sebelum menjalankan program.

### `aturan.py`: angka aturan

[`aturan.py`](./aturan.py) adalah tempat angka aturan koperasi:

- `BATAS_PER_BARANG = 5`: satu siswa boleh membeli paling banyak lima buah dari barang yang sama, dihitung dari pembelian yang belum dibatalkan.
- `DISKON_MULAI = 10000`: subtotal minimal untuk mulai mendapat diskon.
- `DISKON_PERSEN = 10`: diskon sebesar 10 persen.

README menekankan bahwa angka aturan hanya boleh berada di file ini. Jadi saat menulis logika diskon atau batas, gunakan `aturan.BATAS_PER_BARANG`, `aturan.DISKON_MULAI`, dan `aturan.DISKON_PERSEN`, bukan menyalin angka tersebut ke `koperasi.py`.

### `db/schema.sql` dan `db/seed.sql`: struktur dan data

[`db/schema.sql`](./db/schema.sql) membuat tiga tabel:

| Tabel | Isi | Kolom penting |
|---|---|---|
| `students` | Siswa | `id`, `name`, `balance` |
| `items` | Barang koperasi | `id`, `name`, `price`, `stock` |
| `purchases` | Riwayat pembelian | `id`, `student_id`, `item_id`, `qty`, `total`, `status` |

Relasinya:

```text
students.id ─── purchases.student_id
items.id    ─── purchases.item_id
```

Satu baris di `purchases` berarti seorang siswa membeli satu jenis barang dalam jumlah tertentu. `total` menyimpan uang yang benar-benar dibayar untuk pembelian itu, setelah diskon jika ada. `status` berisi `ok` untuk pembelian aktif atau `batal` untuk pembelian yang dibatalkan.

[`db/seed.sql`](./db/seed.sql) mengisi data awal. Contohnya, Andi memiliki saldo 30000; Pensil berharga 2000 dan memiliki stok 30. Data awal ini dipakai ketika menguji program, bukan nilai yang harus ditulis tetap di logika.

### `cek.py` dan `contoh/`: penguji

[`cek.py`](./cek.py) membaca pasangan berkas masukan dan keluaran yang diharapkan dari folder `contoh/`. Untuk setiap contoh, skrip:

1. menjalankan ulang skema dan data awal;
2. menjalankan program dengan input contoh;
3. membandingkan keluaran program dengan keluaran yang diharapkan;
4. melaporkan contoh yang lulus atau gagal.

Karena database di-reset setiap contoh, perubahan dari satu contoh tidak terbawa ke contoh berikutnya. Enam contoh yang disediakan hanya sebagian kecil dari skenario penilaian. Berkas [`coba.py`](./coba.py) adalah contoh kecil untuk melihat perubahan saldo setelah memanggil `isi`.

## 3. Cara kerja data pada tiga tabel

Bayangkan Andi membeli dua Pensil:

1. Program mencari `Andi` di `students` untuk mengetahui ID dan saldonya.
2. Program mencari `Pensil` di `items` untuk mengetahui ID, harga, dan stoknya.
3. Jika semua pemeriksaan lolos, saldo Andi dikurangi dan stok Pensil dikurangi.
4. Satu baris baru ditambahkan ke `purchases`, berisi ID Andi, ID Pensil, jumlah 2, total yang dibayar, dan status `ok`.

ID dipakai untuk menghubungkan tabel; nama siswa dan nama barang tetap dipakai saat menerima input dan menampilkan laporan. Baris pembelian juga menyimpan riwayat, sehingga laporan, batas pembelian, dan pembatalan dapat menghitung transaksi yang tepat.

Nama harus cocok persis, termasuk huruf besar dan kecil. Misalnya `Andi` dan `andi` adalah nama yang berbeda. Query yang sudah ada menggunakan `BINARY name = %s` agar pencarian nama mengikuti aturan ini.

## 4. Aturan setiap perintah

### `isi NAMA NOMINAL`

Urutan:

1. Cari siswa.
2. Jika tidak ada, cetak `Siswa tidak ditemukan` dan berhenti.
3. Pastikan nominal adalah bilangan bulat minimal 1.
4. Jika tidak valid, cetak `Nominal tidak valid` dan berhenti.
5. Tambahkan nominal ke saldo siswa.
6. Jika berhasil, jangan cetak apa pun.

Pengecekan siswa harus lebih dahulu. Jika nama siswa tidak ada dan nominal juga tidak valid, pesan yang benar tetap `Siswa tidak ditemukan`.

### `saldo NAMA`

1. Cari siswa berdasarkan nama persis.
2. Jika tidak ada, cetak `Siswa tidak ditemukan`.
3. Jika ditemukan, cetak dalam format `Andi saldo : 30000`.

Saldo harus dibaca dari database saat perintah dijalankan, karena perintah `isi`, `beli`, dan `batal` sebelumnya mungkin sudah mengubahnya.

### `beli NAMA BARANG JUMLAH`

Pemeriksaan wajib berhenti pada kegagalan pertama dan dilakukan dalam urutan ini:

1. Siswa ada? Jika tidak: `Siswa tidak ditemukan`.
2. Barang ada? Jika tidak: `Barang tidak ditemukan`.
3. Jumlah bilangan bulat minimal 1? Jika tidak: `Jumlah tidak valid`.
4. Jumlah pembelian aktif siswa untuk barang tersebut ditambah jumlah baru tidak melebihi batas? Jika tidak: `Melebihi batas pembelian`.
5. Stok cukup? Jika tidak: `Stok tidak cukup`.
6. Saldo cukup untuk membayar? Jika tidak: `Saldo tidak cukup`.

Setelah semua pemeriksaan lolos:

1. Hitung subtotal = harga × jumlah.
2. Jika subtotal mencapai atau melewati `aturan.DISKON_MULAI`, hitung diskon dengan `aturan.DISKON_PERSEN`.
3. Kurangi saldo sebesar total setelah diskon.
4. Kurangi stok sebesar jumlah barang.
5. Catat satu pembelian dengan jumlah dan total yang benar-benar dibayar.

Saldo yang persis sama dengan total bayar cukup; kegagalannya hanya jika saldo kurang. Pembelian yang berhasil mendapat nomor dari ID otomatis pada tabel `purchases`. Pembelian gagal tidak boleh membuat catatan, mengurangi saldo, atau mengurangi stok.

**Contoh hitung:** harga barang 2000 dan jumlah 5 menghasilkan subtotal 10000. Karena subtotal mencapai ambang 10000, diskon berlaku. Diskon 10% adalah 1000, jadi total yang dibayar 9000. Nilai `total` pada tabel pembelian sebaiknya mewakili 9000, sebab nilai itulah yang harus dikembalikan jika transaksi dibatalkan.

Saat menghitung batas per barang, hanya hitung baris pembelian siswa dan barang yang statusnya masih aktif (`ok`). Pembelian berstatus `batal` tidak ikut dihitung.

### `laporan`

Laporan menampilkan satu baris untuk setiap barang, termasuk barang yang belum pernah terjual:

```text
Pensil 3 buah pendapatan : 6000
```

Untuk setiap barang, jumlahkan kuantitas dan pendapatan dari pembelian aktif saja. Pendapatan adalah jumlah kolom `total`, bukan harga dikali jumlah secara baru—kolom `total` sudah menyimpan pembayaran setelah diskon.

Urutannya:

1. pendapatan tertinggi lebih dahulu;
2. jika pendapatan sama, nama barang urut A sampai Z.

Baris terakhir adalah jumlah kuantitas dan pendapatan seluruh barang, misalnya:

```text
TOTAL 3 buah pendapatan : 6000
```

Barang tanpa transaksi perlu tetap muncul dengan kuantitas 0 dan pendapatan 0. Berhati-hatilah saat menggunakan `JOIN`: jika query hanya menghasilkan barang yang punya baris pembelian, barang yang belum terjual akan hilang. Pikirkan cara agar semua baris `items` tetap menjadi dasar laporan.

### `stok` (bonus)

Cetak setiap barang dalam urutan ID barang, bukan urutan alfabetis:

```text
Buku_Tulis stok : 20
```

Fungsi ini hanya membaca nama dan stok dari `items`; tidak mengubah database.

### `batal NOMOR` (bonus)

Urutannya:

1. Pastikan nomor berupa bilangan bulat minimal 1 dan pembelian dengan ID tersebut ada. Jika tidak: `Pembelian tidak ditemukan`.
2. Jika pembelian sudah berstatus `batal`, cetak `Pembelian sudah dibatalkan`.
3. Jika masih aktif, ubah status menjadi `batal`, kembalikan saldo sebesar nilai `total` pembelian, dan tambahkan kembali `qty` ke stok barang.
4. Jika berhasil, jangan cetak apa pun.

Pengembalian uang menggunakan total yang dahulu dibayar setelah diskon. Jangan menghitung ulang harga × jumlah untuk pengembalian, karena hasilnya dapat berbeda dari jumlah yang dibayar.

## 5. Kondisi `koperasi.py` sekarang

Di [`koperasi.py`](./koperasi.py):

- `isi` sudah berisi pencarian siswa, validasi nominal, dan penambahan saldo.
- `saldo` sudah berisi pencarian siswa dan pencetakan saldo.
- `beli`, `laporan`, `stok`, dan `batal` masih berupa TODO/`pass`, sehingga belum menjalankan tugasnya.

Dua fungsi yang sudah ada dapat dijadikan contoh pola: baca data memakai `fetch_all`, cek apakah hasilnya kosong, lalu tampilkan pesan atau jalankan `execute`. Untuk update saldo, `execute` menerima SQL dan parameter secara terpisah.

## 6. Langkah mengerjakan `koperasi.py` dengan hint

Berikut urutan yang disarankan. Kerjakan satu fungsi, lalu uji, sebelum berpindah ke fungsi berikutnya.

### Langkah 1 — Pastikan lingkungan siap

README menyarankan MySQL berjalan, konfigurasi pengguna di `db.py` sesuai ID, lalu menjalankan:

```text
uv run cek.py
```

Contoh awal memang bisa gagal karena beberapa fungsi masih kosong. Jangan langsung mengubah `main.py` atau berkas SQL untuk membuat contoh lulus; tugas utama adalah mengisi fungsi yang ditandai TODO di `koperasi.py`.

**Hint:** sebelum menulis fungsi, lihat nama kolom dan relasi di `db/schema.sql`, konstanta di `aturan.py`, serta bentuk pemanggilan di `main.py`. Dengan begitu, nama tabel dan tipe input tidak perlu ditebak.

### Langkah 2 — Pahami pola baca dan ubah database

Untuk mencari data, gunakan `fetch_all` dan periksa hasilnya sebelum membaca elemen pertama. Jika hasil query kosong, objek yang dicari tidak ditemukan. Untuk mengubah data, gunakan `execute` dengan placeholder SQL dan parameter.

**Hint:** data dari `fetch_all` berbentuk dictionary karena koneksi menggunakan cursor dengan `dictionary=True`. Gunakan nama kolom, seperti `siswa[0]["id"]`, bukan indeks kolom seperti `[0][0]`.

### Langkah 3 — Lengkapi `isi` dan uji aturannya

Bandingkan implementasi yang ada dengan urutan di README:

1. cari siswa;
2. validasi nominal sebagai bilangan bulat positif;
3. update saldo.

Uji setidaknya nama ada/tidak ada dan nominal valid, nol, negatif, teks, serta bilangan desimal. Contoh pesan harus persis, termasuk huruf besar-kecil.

**Hint:** input dari `main.py` berupa string. Konversi ke `int` dapat gagal untuk teks seperti `abc` atau `1.5`; tempatkan konversi di penanganan error yang sesuai. Jangan melakukan update sebelum semua validasi lulus.

### Langkah 4 — Lengkapi `saldo`

Pastikan satu query mengambil nama dan saldo. Jika tidak ada hasil, cetak pesan siswa tidak ditemukan; jika ada, format keluaran harus cocok, termasuk spasi sebelum dan sesudah titik dua.

**Hint:** gunakan nama yang diperoleh dari database untuk format keluaran, agar kapitalisasi yang ditampilkan mengikuti nama siswa yang tersimpan.

### Langkah 5 — Rancang `beli` sebagai validasi berurutan

Sebelum menulis SQL perubahan, tulis dulu keenam pemeriksaan di kertas atau sebagai daftar kerja. Terapkan benar-benar sesuai urutan README. Setiap kegagalan mencetak satu pesan lalu langsung berhenti.

**Hint untuk tiap pemeriksaan:**

- siswa: cari ID dan saldo dengan nama persis;
- barang: cari ID, harga, dan stok;
- jumlah: ubah teks menjadi bilangan bulat positif;
- batas: jumlahkan pembelian `ok` milik siswa tersebut untuk barang yang sama, lalu tambahkan jumlah baru;
- stok: bandingkan stok dengan jumlah yang diminta;
- saldo: hitung subtotal dan total bayar setelah diskon, lalu bandingkan saldo dengan total itu.

Hanya setelah keenam pemeriksaan lolos, lakukan perubahan saldo, stok, dan catatan pembelian. Bila ada kegagalan, tidak boleh ada satu pun data yang berubah.

**Hint SQL:** pencarian jumlah pembelian aktif memerlukan `purchases`, dengan filter siswa, barang, dan `status = 'ok'`. Untuk pencatatan pembelian, lihat kolom wajib dan foreign key di `schema.sql`.

**Hint hitungan:** periksa diskon ketika subtotal `>= aturan.DISKON_MULAI`, bukan hanya ketika lebih besar. Semua nilai keluaran dan nilai uang yang disimpan harus bilangan bulat. Saldo yang sama persis dengan total bayar berarti cukup.

### Langkah 6 — Buat `laporan`

Mulai dari daftar semua barang, lalu hubungkan pembelian aktif dan hitung total kuantitas serta pendapatan per barang. Urutkan hasil dengan pendapatan menurun dan nama menaik sebagai pemecah nilai seri. Hitung total keseluruhan untuk baris terakhir.

**Hint SQL:** pikirkan `LEFT JOIN` agar barang tanpa pembelian tetap muncul. Pembelian batal harus dikeluarkan dari agregasi. Gunakan jumlah `qty` untuk banyak buah dan jumlah `total` untuk pendapatan. Pastikan nilai kosong dari agregasi ditampilkan sebagai nol, bukan teks `None`.

### Langkah 7 — Buat `stok` (bonus)

Ambil semua barang dengan nama dan stok, urutkan berdasarkan `id`, kemudian cetak satu baris per barang sesuai format README.

**Hint:** fungsi ini hanya perlu membaca data; jangan membuat update atau mengubah tabel.

### Langkah 8 — Buat `batal` (bonus)

Validasi nomor dan keberadaan pembelian terlebih dahulu. Setelah ada, cek statusnya. Hanya pembelian aktif yang boleh diproses.

**Hint:** ambil data pembelian yang dibutuhkan dalam satu pencarian: ID pembelian, ID siswa, ID barang, jumlah, total, dan status. Gunakan `total` untuk mengembalikan saldo serta `qty` untuk menambah stok. Pembelian batal kedua kalinya harus menghasilkan pesan khusus tanpa perubahan tambahan.

### Langkah 9 — Uji urutan dan kasus tepi

Jalankan `uv run cek.py` setelah menyelesaikan fungsi. Jika gagal, baca baris “seharusnya” dan “programmu”, lalu cocokkan dengan aturan. Selain enam contoh yang tersedia, buat input uji sendiri untuk kasus seperti:

- nama salah kapitalisasi;
- nominal atau jumlah `0`, negatif, teks, atau desimal;
- stok tepat sama dengan jumlah yang dibeli;
- saldo tepat sama dengan total setelah diskon;
- subtotal tepat di ambang diskon;
- jumlah pembelian mencapai batas, lalu melewatinya;
- transaksi dibatalkan lalu barang dibeli lagi;
- laporan barang tanpa penjualan;
- pembatalan nomor tidak ada dan pembatalan dua kali.

Ingat, `cek.py` mengatur ulang database sebelum tiap contoh. Jika kamu menguji beberapa perintah yang harus berbagi keadaan—misalnya beli lalu batal—masukkan kedua perintah dalam satu input uji.

## 7. Ringkasan mental model

Saat membaca atau menulis kode, pikirkan pertanyaan ini:

1. **Siapa yang memilih fungsi?** `main.py`.
2. **Di mana aturan dan pengecekan dilakukan?** `koperasi.py`, memakai angka dari `aturan.py`.
3. **Siapa yang berbicara dengan database?** `db.py`.
4. **Di mana data disimpan?** Tabel `students`, `items`, dan `purchases`.
5. **Apa syarat operasi aman?** Semua pengecekan dilakukan berurutan sebelum perubahan data.
6. **Apa yang membedakan transaksi aktif dan batal?** Kolom `purchases.status`; hanya status `ok` dihitung sebagai transaksi aktif.

Jika enam pertanyaan ini jelas, hubungan antarfile dan alur tugas akan lebih mudah diikuti.

## 8. Penjelasan detail kode yang sudah dikerjakan

Bagian ini menjelaskan implementasi yang sekarang ada di [`koperasi.py`](./koperasi.py), termasuk arti variabel, cara mengambil data hasil query, dan alasan urutan langkahnya.

### 8.1 Cara membaca hasil `fetch_all`

`fetch_all` mengembalikan daftar baris. Karena `db.py` membuat cursor dengan `dictionary=True`, setiap baris berupa dictionary yang kuncinya adalah nama kolom. Contoh bentuk hasil query siswa:

```python
[
    {"id": 1, "balance": 30000}
]
```

Pada contoh tersebut:

- `siswa` adalah daftar hasil query;
- `siswa[0]` berarti baris pertama di daftar;
- `siswa[0]["id"]` berarti nilai kolom `id` dari baris pertama, yaitu `1`;
- `siswa[0]["balance"]` berarti saldo dari baris pertama, yaitu `30000`.

Jadi `siswa[0]["id"]` bukan sintaks khusus database. Itu dua langkah akses Python yang dirangkai: pilih baris pertama dari list, kemudian pilih nilai berdasarkan kunci dictionary.

Cara yang lebih singkat, tetapi tidak wajib, adalah menyimpan baris pertama ke variabel lain:

```python
data_siswa = siswa[0]
id_siswa = data_siswa["id"]
```

Kode tugas ini memilih cara langsung seperti `siswa[0]["id"]`. Itu sah dan hasilnya sama. Yang perlu diingat: akses indeks `[0]` hanya aman setelah memastikan hasil query tidak kosong dengan `if not siswa:`.

### 8.2 Parameter SQL dan tuple

Pola seperti ini muncul di fungsi-fungsi:

```python
fetch_all(
    "SELECT id, balance FROM students WHERE BINARY name = %s",
    (nama,)
)
```

String pertama adalah SQL. `%s` adalah tempat nilai parameter dimasukkan oleh driver MySQL. String kedua, `(nama,)`, adalah tuple berisi satu nilai. Koma setelah `nama` penting: `(nama)` saja bukan tuple, melainkan nilai `nama yang hanya diberi tanda kurung.

Kalau ada dua nilai, tuple-nya berisi dua elemen, misalnya `(id_siswa, id_barang)`. Nilai parameter dipisahkan dari teks SQL agar driver dapat mengirimkannya dengan benar.

### 8.3 `isi`: menambahkan saldo

Alur fungsi `isi` adalah:

1. Query mencari `id` siswa berdasarkan nama. `BINARY name = %s` meminta kecocokan huruf yang persis, jadi `Andi` berbeda dari `andi`.
2. `if not siswa` memeriksa apakah daftar hasil kosong. Kalau kosong, siswa tidak ditemukan; pesan dicetak dan `return` menghentikan fungsi.
3. `int(nominal)` mencoba mengubah teks nominal menjadi integer. Misalnya `"1000"` menjadi `1000`.
4. `except ValueError` menangani teks yang tidak bisa menjadi integer, misalnya `"abc"` atau `"1.5"`.
5. `if jumlah < 1` menolak nol dan angka negatif.
6. `execute` menambah saldo dengan operasi SQL `balance = balance + %s`, hanya pada siswa dengan ID yang ditemukan.

Tidak ada `print` setelah update karena keberhasilan `isi` memang tidak boleh menghasilkan pesan.

### 8.4 `saldo`: membaca saldo siswa

Fungsi ini meminta dua kolom: `name` dan `balance`. Hasilnya tetap berbentuk daftar dictionary. Jika tidak ada siswa, fungsi mencetak pesan lalu berhenti. Kalau ada, ekspresi `siswa[0]["name"]` dan `siswa[0]["balance"]` mengambil nama serta saldo dari baris pertama.

`f'...'` adalah f-string: ekspresi di dalam kurung kurawal `{}` dihitung dan hasilnya dimasukkan ke teks. Karena itu satu baris tersebut menghasilkan format seperti `Andi saldo : 30000`.

### 8.5 `beli`: validasi, hitung, lalu simpan

Fungsi `beli` paling panjang karena ia harus memastikan transaksi aman sebelum mengubah saldo atau stok.

#### A. Mencari siswa dan barang

Query pertama memilih `id` dan `balance` siswa. ID diperlukan untuk memperbarui saldo dan menghubungkan pembelian ke siswa; saldo diperlukan untuk memastikan uangnya cukup.

Setelah itu query barang memilih `id`, `price`, dan `stock`:

- `id` diperlukan untuk memperbarui stok dan mencatat barang pada transaksi;
- `price` dipakai untuk menghitung subtotal;
- `stock` dipakai untuk mengecek ketersediaan.

Pemeriksaan siswa dilakukan sebelum barang, dan barang sebelum jumlah, sesuai urutan pesan kesalahan pada tugas. Setiap `return` membuat fungsi berhenti pada kesalahan pertama.

#### B. Mengubah dan memvalidasi jumlah

`main.py` meneruskan setiap kata input sebagai teks. Maka `jumlah` yang masuk ke fungsi awalnya string. `int(jumlah)` mengubah string angka seperti `"2"` menjadi angka `2`; blok `try`/`except` menangani teks yang tidak bisa dikonversi. Setelah itu, pemeriksaan `jumlah < 1` menolak nol dan bilangan negatif.

Setelah validasi ini, variabel `jumlah` sudah berisi integer. Nilai ini dipakai untuk hitungan batas pembelian, pengecekan stok, dan perubahan stok.

#### C. Menghitung pembelian aktif sebelumnya

Query `pembelian_lama` mencari jumlah `qty` dari pembelian siswa dan barang yang sama, tetapi hanya yang `status = 'ok'`.

- `SUM(qty)` menjumlahkan kuantitas dari beberapa transaksi.
- `COALESCE(..., 0)` membuat hasilnya nol jika siswa belum pernah membeli barang tersebut.
- `AS total_qty` memberi nama pada hasil hitungan agar dapat diakses sebagai `pembelian_lama[0]["total_qty"]`.

`jumlah_sebelumnya` mengambil angka hasil query itu. Kode membandingkan `jumlah_sebelumnya + jumlah` dengan `aturan.BATAS_PER_BARANG`. Jika jumlah baru membuat batas terlampaui, fungsi mencetak pesan dan berhenti. Pembelian berstatus `batal` tidak ikut menghitung batas.

#### D. Mengecek stok dan menghitung harga

`daftar_barang[0]["stock"]` berarti nilai stok dari baris barang pertama yang ditemukan. Jika stok lebih kecil daripada jumlah yang ingin dibeli, fungsi mencetak `Stok tidak cukup` dan berhenti.

Setelah stok cukup:

```text
subtotal = harga satuan x jumlah
```

`diskon` dimulai dari nol. Jika subtotal mencapai atau melewati `aturan.DISKON_MULAI`, diskon dihitung dari persentase di `aturan.DISKON_PERSEN`. Kemudian:

```text
total_bayar = subtotal - diskon
```

Nilai `total_bayar` itulah yang dibandingkan dengan `siswa[0]["balance"]`. Jika saldo lebih kecil, pembelian gagal. Saldo yang sama persis dengan total bayar masih cukup.

#### E. Menyimpan pembelian yang lolos

Tiga pemanggilan `execute` di akhir fungsi melakukan perubahan:

1. mengurangi `students.balance` sebesar `total_bayar`;
2. mengurangi `items.stock` sebesar `jumlah`;
3. menambahkan satu baris ke `purchases`, berisi ID siswa, ID barang, jumlah, dan total setelah diskon.

Ketiganya hanya dijalankan setelah semua pemeriksaan lolos. Dengan begitu, kegagalan validasi tidak mengubah data. `purchases.total` harus menyimpan uang yang benar-benar dibayar setelah diskon, sebab nilai itu dipakai untuk mengembalikan saldo jika pembelian dibatalkan.

Pada `db.py` yang disediakan, setiap `execute` melakukan `commit` sendiri. Artinya, program tidak menggabungkan ketiga perubahan tersebut menjadi satu transaksi database yang atomik. Untuk tugas ini, pola yang dipakai adalah menyelesaikan seluruh validasi terlebih dahulu, baru menjalankan perubahan.

### 8.6 `laporan`: menggabungkan barang dan penjualan

Query laporan dimulai dari tabel `items`, lalu memakai `LEFT JOIN` ke `purchases`. `LEFT JOIN` penting karena barang harus tetap tampil meskipun belum punya transaksi. Kondisi `p.status = 'ok'` ditaruh pada bagian `ON`, sehingga pembelian batal tidak bergabung sebagai penjualan, tetapi barang tanpa pembelian tetap ada.

`SUM(p.qty)` menghitung jumlah barang terjual; `SUM(p.total)` menghitung pendapatan yang benar-benar dibayar. Keduanya dibungkus `COALESCE(..., 0)` supaya barang tanpa penjualan mendapat angka nol.

`GROUP BY i.id, i.name` menggabungkan baris transaksi menjadi satu hasil per barang. `ORDER BY pendapatan DESC, i.name ASC` berarti pendapatan tertinggi lebih dahulu; jika sama, nama barang urut naik.

Setelah query selesai, perulangan `for barang in data_barang` berjalan satu kali untuk setiap barang. `int(...)` memastikan angka dicetak sebagai integer. F-string menyusun baris sesuai format. Di dalam perulangan, `jumlah_total` dan `pendapatan_total` terus ditambah; setelah perulangan selesai, keduanya dicetak pada baris `TOTAL`.

### 8.7 `stok`: membaca daftar stok

Query memilih `name` dan `stock`, lalu `ORDER BY id` mengurutkan barang sesuai ID. Perulangan `for` mengambil satu dictionary barang setiap kali. `barang["name"]` dan `barang["stock"]` adalah akses ke kolom dari baris tersebut. Fungsi ini hanya membaca data dan tidak menjalankan `execute`.

### 8.8 `batal`: membatalkan dan mengembalikan barang serta uang

Nomor pembelian datang sebagai teks. `int(nomor)` mengubahnya menjadi integer; jika gagal, `except` mencetak `Pembelian tidak ditemukan`. Nomor di bawah 1 juga ditolak.

Query pembelian mengambil `id`, `student_id`, `item_id`, `qty`, `total`, dan `status`. Semua kolom tersebut diperlukan untuk menentukan status transaksi dan melakukan pengembalian. Jika daftar kosong, ID pembelian tidak ada. Jika statusnya sudah `batal`, fungsi mencetak pesan khusus dan berhenti sebelum melakukan perubahan.

Untuk pembelian aktif, tiga update melakukan hal berikut:

1. mengubah status pembelian menjadi `batal`;
2. menambah saldo siswa memakai `pembelian[0]["total"]`, yaitu uang yang benar-benar dibayar;
3. menambah stok barang memakai `pembelian[0]["qty"]`, yaitu jumlah barang yang dahulu dibeli.

Penting bahwa pengembalian uang menggunakan `total` tersimpan, bukan menghitung harga dan diskon ulang. Pembelian yang dibatalkan tetap tersimpan sebagai riwayat; statusnya saja yang berubah.

### 8.9 Ringkasan cara berpikir saat membaca kode

Untuk setiap fungsi, ikuti alur ini:

1. **Query apa yang dipanggil?** Periksa tabel dan kolom yang diminta.
2. **Bentuk hasilnya apa?** `fetch_all` menghasilkan list berisi dictionary.
3. **Apa arti akses datanya?** Misalnya `siswa[0]["id"]`: baris pertama, kolom `id`.
4. **Validasi apa yang dilakukan?** Perhatikan urutannya dan `return` yang menghentikan proses.
5. **Kapan database berubah?** Cari pemanggilan `execute`; pada `beli`, semuanya berada setelah pemeriksaan.
6. **Apa yang dicetak?** Periksa format string dan pastikan operasi yang berhasil memang tidak mencetak pesan jika aturan meminta diam.
