# Hari 1 — Hands-on: bangun sakura-tasks

Ikuti langkahnya berurutan, ketik persis, dan cocokkan hasilmu di setiap titik cek. Penjelasan disampaikan trainer sambil mengetik.

## Tujuan 2 hari

Di akhir Hari 2, **semua peserta punya hasil yang sama**: aplikasi pencatat tugas `sakura-tasks` yang jalan di Ubuntu (WSL), tersimpan di GitHub, dan ada tesnya. Hari 3 dipakai untuk tugas mandiri.

### Hasil akhir yang dikejar (akhir Hari 2)

Isi folder proyek:

```text
sakura-tasks/
  main.py            program yang dijalankan
  tugas.py           class Tugas dan PengelolaTugas (modul)
  tasks.json         data tugas, dibuat otomatis saat program jalan
  tests/
    test_tugas.py    tes otomatis dengan pytest
  pyproject.toml     identitas proyek
```

Program dijalankan dari terminal Ubuntu, di folder `~/sakura-tasks`:

```text
uv run main.py
```

Lalu di dalam program (baris yang diawali tanda `>`):

```text
sakura-tasks. Perintah: add JUDUL, list, done NOMOR, stats, keluar
> add bangun pagi
Ditambahkan: bangun pagi
> done 1
Selesai: bangun pagi
> keluar
```

Jalankan lagi `uv run main.py`. Tugasnya **masih ada**, karena tersimpan di `tasks.json`:

```text
> list
1. [x] bangun pagi
```

Dan semua tes lulus:

```text
uv run pytest
```

### Cara membaca perintah di dalam program

Baris yang diawali `>` diketik **di dalam program**, bukan di terminal Ubuntu. Satu perintah terdiri dari kata perintah, lalu isinya kalau perlu.

| Ketik | Artinya |
| --- | --- |
| `add bangun pagi` | Tambah tugas berjudul "bangun pagi". `add` = perintah, `bangun pagi` = judul tugasnya |
| `list` | Tampilkan semua tugas |
| `done 1` | Tandai tugas nomor 1 selesai |
| `stats` | Tampilkan ringkasan jumlah |
| `keluar` | Keluar dari program, kembali ke terminal Ubuntu |

### Hasil per hari

| Hari | Hasil di akhir hari |
| --- | --- |
| Hari 1 (hari ini) | `main.py` interaktif dengan perintah `add`, `list`, `done`, `stats`, `keluar`. Satu commit, repo private di GitHub |
| Hari 2 | Kode yang sama dirapikan: `tugas.py` berisi class, data tersimpan di `tasks.json`, tes pytest lulus. Di-push ke repo yang sama |

## Persiapan sebelum mulai

- [ ] Laptop terhubung internet dan baterai aman untuk 2 jam
- [ ] Aplikasi **Ubuntu** terbuka dari menu Windows (bukan PowerShell)
- [ ] Python 3.12, `uv`, dan `git` sudah terpasang (dicek di Bagian A)
- [ ] VS Code terpasang beserta ekstensi WSL
- [ ] Akun GitHub dan kunci SSH sudah jalan dari Minggu 1
- [ ] Aku tahu ID pesertaku (P01 sampai P25)

## Peta Hari 1 (115 menit)

| Bagian | Isi | Menit | Hasilnya |
| --- | --- | --- | --- |
| A | Orientasi WSL | 20 | Tahu posisi di terminal, folder rumah `~` dikenali |
| B | Proyek pertama | 15 | Folder `sakura-tasks`, program menyapa jalan |
| C | List dan perulangan | 15 | Tugas tampil bernomor |
| D | Fungsi | 15 | `tambah` dan `tampilkan` |
| E | Program interaktif | 20 | Perintah `add`, `list`, `keluar` |
| F | Selesai dan statistik | 15 | Perintah `done`, `stats`. `main.py` final Hari 1 |
| G | Git dan GitHub | 15 | Commit dan push ke repo private |

## Aturan main

1. Ikuti bagian dari A sampai G, berurutan.
2. Ketik hanya isi kotak **Ketik**. Sisanya dibaca saja.
3. Setiap bagian ditutup **Titik cek**. Cocok? Lanjut.
4. Tertinggal? Pakai **Jalur kejar** di bagian bawah, tidak perlu menunggu siapa pun.
5. Stuck? Tulis di grup: ID, bagian, dan tempel pesan error. Contoh: "P08 stuck di E1".

## Cara membaca lembar ini

Setiap langkah punya pola yang sama, dan kamu hanya mengetik isi kotak berlabel **Ketik**. Hal lain di lembar ini dibaca saja.

| Label | Artinya |
| --- | --- |
| **Folder** | Tempat kamu harus berada saat mengetik |
| **File** | Nama file beserta lokasinya. "Baru" berarti kamu yang membuatnya |
| **Ketik** | Persis inilah yang diketik, tidak lebih dan tidak kurang |
| **Jalankan** | Perintah untuk menjalankan, diketik di terminal Ubuntu |
| **Yang harus muncul di layar** | Hanya dibaca. Jangan diketik |
| **Titik cek** | Cocokkan hasilmu sebelum lanjut |

**Contoh salah dan benar.** Kalau lembar menyuruh menampilkan isi folder, yang diketik hanya ini:

```text
ls -lah
```

Kalimat "menampilkan isi folder" adalah penjelasan, bukan bagian perintah. Kalau penjelasan ikut diketik di terminal, tanda `>` membuat Ubuntu menulis hasilnya ke file baru bernama `menampilkan`, dan muncul pesan error.

### Membaca posisi dari prompt

Bagian di antara `:` dan `$` pada prompt adalah **folder tempat kamu berada sekarang**.

```text
nama@LAPTOP:~/sakura-tasks$
```

| Tertulis di prompt | Alamat lengkapnya |
| --- | --- |
| `~` | `/home/nama` |
| `~/sakura-tasks` | `/home/nama/sakura-tasks` |
| `~/sakura-tasks/main.py` | `/home/nama/sakura-tasks/main.py` |

Tanda `~` artinya rumahmu di Ubuntu. Kata `nama` diganti nama penggunamu; cek dengan perintah `whoami`.

### Membaca alamat file

`/home/nama/sakura-tasks/main.py` dibaca dari kiri ke kanan: folder `home`, lalu `nama` (rumahmu), lalu `sakura-tasks` (folder proyek), dan terakhir file `main.py`.

### Kamus mini

Penjelasannya akan disampaikan trainer sambil mengetik. Tabel ini untuk dibuka kalau kamu ketemu kata yang belum kamu pahami.

| Kata | Artinya | Contoh |
| --- | --- | --- |
| variabel | Wadah bernama untuk menyimpan nilai | `nama = "Bayu"` |
| `print` | Menampilkan teks ke layar | `print("Halo")` |
| `input` | Meminta pengguna mengetik sesuatu | `input("Siapa namamu? ")` |
| list | Daftar berurutan | `tugas = []` |
| `for` dan `while` | Mengulang kode | `for item in tugas:` |
| `if` dan `else` | Memilih jalan | `if nomor < 1:` |
| dictionary | Data berpasangan nama dan nilai | `{"judul": "bangun pagi"}` |
| fungsi | Potongan kode bernama yang bisa dipanggil berulang | `def tambah(judul):` |

### Kalau kamu tertinggal

Kamu tidak perlu menunggu atau memanggil trainer untuk hal yang bisa dikejar sendiri. Buka **Titik cek** terakhir yang berhasil kamu lewati, cocokkan isi file-mu, lalu lanjut ke langkah berikutnya. Kalau sudah lebih dari satu bagian tertinggal, salin isi file dari titik cek bagian sebelumnya ke `main.py`, jalankan, dan lanjut mengetik dari sana. Tanyakan arti kodenya ke temanmu atau trainer setelah kamu mengejar.

---

## Bagian A — Orientasi WSL (20 menit)

Setelah bagian ini kamu tahu sedang berada di terminal yang benar dan di folder mana, serta tahu aturan menyimpan proyek.

### A1 — Buka terminal Ubuntu

1. Tekan tombol Windows di keyboard.
2. Ketik kata `Ubuntu`.
3. Tekan Enter. Jendela hitam terbuka.

**Yang harus terlihat di baris terakhir (prompt):**

```text
nama@LAPTOP:~$
```

Kalau yang terlihat `PS C:\Users\...>`, itu PowerShell. Tutup, lalu buka lagi aplikasi **Ubuntu**.

### A2 — Cek kamu sedang di mana

**Folder:** bebas.

**Ketik** (satu baris, tekan Enter, lalu baris berikutnya):

```text
pwd
whoami
```

**Yang harus muncul di layar** (nama di komputermu berbeda):

```text
/home/nama
nama
```

Baris pertama adalah alamat folder tempatmu berada. Baris kedua adalah nama penggunamu di Ubuntu.

### A3 — Pindah ke folder rumah

**Folder:** bebas.

**Ketik** (satu baris per Enter):

```text
cd ~
pwd
```

**Yang harus muncul di layar:**

```text
/home/nama
```

Prompt-mu sekarang menjadi:

```text
nama@LAPTOP:~$
```

**Aturan emas:** setiap proyek adalah satu folder langsung di bawah `~/`, namanya sama dengan nama proyek. Contoh hari ini: `~/sakura-tasks`. Jangan menyimpannya di `/mnt/c/...`, karena lebih lambat dan sering bermasalah.

### A4 — Cek alat

**Folder:** `~`.

**Ketik:**

```text
python3 --version
uv --version
git --version
```

**Yang harus muncul di layar** (angka di belakang boleh berbeda):

```text
Python 3.12.3
uv 0.5.11
git version 2.43.0
```

Syarat satu-satunya: Python berawalan **3.12**. Kalau bukan, ketik `uv python install 3.12`. Kalau muncul `command not found`, tutup Ubuntu, buka lagi, lalu ulangi.

### A5 — Cek identitas Git dan SSH

**Folder:** `~`.

**Ketik:**

```text
git config --global user.name
git config --global user.email
ssh -T git@github.com
```

**Yang harus muncul di layar:**

```text
P08
123456+namagithub@users.noreply.github.com
Hi namagithub! You've successfully authenticated, but GitHub does not provide shell access.
```

- Baris pertama harus **ID pesertamu** (P01, P02, dan seterusnya), bukan nama asli.
- Kalau SSH bertanya `Are you sure you want to continue connecting`, ketik `yes` lalu Enter.
- Kalau ada baris yang kosong atau gagal, itu pengaturan minggu 1 yang belum beres. Tunjukkan ke trainer.

### Titik cek A

- [ ] Prompt terbaca `nama@LAPTOP:~$` di folder rumah
- [ ] `python3 --version` menampilkan 3.12
- [ ] `git config --global user.name` menampilkan ID pesertamu
- [ ] `ssh -T git@github.com` menampilkan `Hi ...! You've successfully authenticated`

---

## Bagian B — Proyek pertama dan program yang menyapa (15 menit)

Setelah bagian ini kamu punya folder proyek sakura-tasks dan sudah menjalankan program yang kamu ketik sendiri.

### B1 — Buat proyek

**Folder:** `~`

**Ketik** (satu baris per Enter):

```text
uv init sakura-tasks --python 3.12
cd sakura-tasks
ls
```

**Yang harus muncul di layar:**

```text
Initialized project `sakura-tasks` at `/home/nama/sakura-tasks`
README.md  main.py  pyproject.toml
```

Urutan tiga nama file di baris terakhir boleh berbeda. Prompt-mu sekarang menjadi `nama@LAPTOP:~/sakura-tasks$`.

| File | Isinya |
| --- | --- |
| `main.py` | Program Python-mu. Di sinilah kamu mengetik hari ini |
| `pyproject.toml` | Identitas proyek: nama, versi, versi Python |
| `README.md` | Catatan perkenalan proyek |

### B2 — Buka proyek di VS Code

**Folder:** `~/sakura-tasks`

**Ketik:**

```text
code .
```

**Yang harus terlihat:**

- VS Code terbuka. Panel kiri menampilkan `main.py`, `pyproject.toml`, `README.md`.
- Pojok kiri bawah tertulis **WSL: Ubuntu**. Kalau tidak, tutup VS Code dan ulangi `code .` dari terminal Ubuntu.
- Kalau muncul tawaran memasang ekstensi **Python** atau **WSL**, klik **Install**.

Buka terminal di dalam VS Code dengan menekan Ctrl dan tombol backtick (karakter di kiri angka 1). Prompt-nya sama dengan terminal Ubuntu tadi. Mulai sekarang boleh mengetik perintah di terminal VS Code ini.

### B3 — Jalankan program contoh

**Folder:** `~/sakura-tasks`

**Jalankan:**

```text
uv run main.py
```

**Yang harus muncul di layar:**

```text
Hello from sakura-tasks!
```

Pertama kali, beberapa baris tentang menyiapkan lingkungan bisa muncul di atasnya. Abaikan. `uv run main.py` artinya: jalankan file `main.py` memakai Python milik proyek ini.

### B4 — Program pertamamu

**File:** `/home/nama/sakura-tasks/main.py` (sudah ada; kamu mengganti isinya)

1. Klik `main.py` di panel kiri VS Code.
2. Tekan Ctrl+A untuk memilih semua isinya, lalu tekan Delete.
3. Ketik isi berikut:

**Ketik di dalam main.py:**

```python
print("Selamat datang di sakura-tasks")
nama = input("Siapa namamu? ")
print(f"Halo, {nama}!")
```

4. Simpan dengan Ctrl+S. Titik putih di tab `main.py` harus hilang.

**Jalankan di terminal:**

```text
uv run main.py
```

**Yang harus muncul di layar.** Program berhenti dan menunggu kamu mengetik nama, lalu Enter. Bagian setelah `Siapa namamu? ` adalah yang kamu ketik sendiri (di sini `Bayu`):

```text
Selamat datang di sakura-tasks
Siapa namamu? Bayu
Halo, Bayu!
```

Jalankan sekali lagi dengan namamu sendiri.

**Kata baru:** variabel (`nama`), `print`, `input`, dan teks berawalan `f` yang mengisi nilai ke dalam `{...}`.

### Titik cek B

- [ ] Folder `~/sakura-tasks` ada dan terbuka di VS Code dengan WSL: Ubuntu
- [ ] `uv run main.py` menyapa namamu
- [ ] Isi `main.py` persis tiga baris di atas

---

## Bagian C — Daftar tugas dengan list dan perulangan (15 menit)

Setelah bagian ini programmu menyimpan beberapa tugas dalam satu daftar dan menampilkannya bernomor.

### C1 — Ganti isi main.py

**Folder:** `~/sakura-tasks`

**File:** `/home/nama/sakura-tasks/main.py` (sudah ada; kamu mengganti isinya)

1. Klik `main.py` di VS Code, tekan Ctrl+A, lalu Delete.
2. Ketik isi berikut. Baris kosong di antaranya ikut diketik, cukup tekan Enter.

**Ketik di dalam main.py:**

```python
tugas = []

tugas.append("bangun pagi")
tugas.append("sarapan")

for nomor, judul in enumerate(tugas, start=1):
    print(f"{nomor}. [ ] {judul}")
```

Baris `print` harus **menjorok 4 spasi** dari baris `for`. Menekan Tab di VS Code menghasilkan 4 spasi. Simpan dengan Ctrl+S.

**Jalankan di terminal:**

```text
uv run main.py
```

**Yang harus muncul di layar:**

```text
1. [ ] bangun pagi
2. [ ] sarapan
```

### C2 — Coba sendiri

Tambahkan satu baris `tugas.append("...")` dengan tugas buatanmu, di bawah dua baris `append` yang ada. Simpan, jalankan lagi. Harus muncul **tiga** baris.

**Kata baru:** list (`[]`), `append` (menambah ke daftar), `for` (mengulang untuk tiap isi daftar), `enumerate` (memberi nomor).

### Titik cek C

- [ ] Layar menampilkan tugas bernomor mulai dari 1
- [ ] Tugas buatanmu ikut tampil
- [ ] Aku tahu bahwa baris di bawah `for` harus menjorok 4 spasi

---

## Bagian D — Fungsi: bungkus kode supaya bisa dipakai ulang (15 menit)

Setelah bagian ini kode tambah dan tampil tugas dibungkus dalam fungsi, dan tiap tugas menyimpan judul serta status selesai.

### D1 — Ganti isi main.py

**Folder:** `~/sakura-tasks`

**File:** `/home/nama/sakura-tasks/main.py` (ganti seluruh isinya: Ctrl+A, Delete)

**Ketik di dalam main.py:**

```python
tugas = []

def tambah(judul):
    tugas.append({"judul": judul, "selesai": False})
    print(f"Ditambahkan: {judul}")

def tampilkan():
    for nomor, item in enumerate(tugas, start=1):
        tanda = "x" if item["selesai"] else " "
        print(f"{nomor}. [{tanda}] {item['judul']}")

tambah("bangun pagi")
tambah("sarapan")
tampilkan()
```

Baris di dalam `def` menjorok 4 spasi. Baris di dalam `for` menjorok 8 spasi (4 + 4). Dua baris `tanda` dan `print` sejajar. Simpan dengan Ctrl+S.

**Jalankan di terminal:**

```text
uv run main.py
```

**Yang harus muncul di layar:**

```text
Ditambahkan: bangun pagi
Ditambahkan: sarapan
1. [ ] bangun pagi
2. [ ] sarapan
```

### D2 — Coba sendiri

Di paling bawah file, tambahkan satu baris `tambah("...")` dengan tugas buatanmu **sebelum** baris `tampilkan()`. Simpan, jalankan. Harus muncul tiga tugas.

**Kata baru:** `def` (membuat fungsi), `judul` di dalam kurung (bahan yang dikirim ke fungsi), dictionary `{...}` (satu tugas berisi judul dan status), `True/False`.

### Titik cek D

- [ ] Pesan "Ditambahkan: ..." muncul untuk tiap tugas
- [ ] Daftar bernomor tampil setelahnya
- [ ] Aku tahu bahwa fungsi baru jalan ketika dipanggil (`tambah(...)`, `tampilkan()`)

---

## Bagian E — Program interaktif: add, list, keluar (20 menit)

Setelah bagian ini programmu menunggu perintah yang kamu ketik, jadi tugas bisa ditambah kapan saja tanpa mengubah kode.

### E1 — Ganti bagian bawah main.py

**Folder:** `~/sakura-tasks`

**File:** `/home/nama/sakura-tasks/main.py`

Dua fungsi di atas (`tambah` dan `tampilkan`) **tetap**. Yang diganti: hapus tiga baris paling bawah (`tambah("bangun pagi")`, `tambah("sarapan")`, `tampilkan()`), lalu ketik blok baru di bawah fungsi `tampilkan`.

Isi `tambah` juga diubah supaya judul kosong ditolak. Paling aman: ganti seluruh isi file dengan versi lengkap di bawah ini.

**Isi lengkap main.py setelah bagian E:**

```python
tugas = []

def tambah(judul):
    judul = judul.strip()
    if judul == "":
        print("Judul tidak boleh kosong")
        return
    tugas.append({"judul": judul, "selesai": False})
    print(f"Ditambahkan: {judul}")

def tampilkan():
    for nomor, item in enumerate(tugas, start=1):
        tanda = "x" if item["selesai"] else " "
        print(f"{nomor}. [{tanda}] {item['judul']}")

print("sakura-tasks. Perintah: add JUDUL, list, keluar")
while True:
    perintah = input("> ")
    if perintah == "keluar":
        break
    elif perintah == "list":
        tampilkan()
    elif perintah.startswith("add "):
        tambah(perintah[4:])
    else:
        print("Perintah tidak dikenal")
```

Perhatikan jorokan: `while True:` rata kiri; semua di dalamnya menjorok 4 spasi; `break`, `tampilkan()`, `tambah(...)`, dan `print` di bawah `if/elif/else` menjorok 8 spasi. Simpan dengan Ctrl+S.

**Jalankan di terminal:**

```text
uv run main.py
```

Program berhenti dan menunggu tanda `>`. Ketik perintah di bawah, satu per satu, tekan Enter tiap baris. Perintah ini diketik di dalam program, bukan di terminal Ubuntu.

**Ketik di dalam program (setelah tanda >):**

```text
add bangun pagi
add sarapan
list
foo
keluar
```

**Yang harus muncul di layar:**

```text
sakura-tasks. Perintah: add JUDUL, list, keluar
> add bangun pagi
Ditambahkan: bangun pagi
> add sarapan
Ditambahkan: sarapan
> list
1. [ ] bangun pagi
2. [ ] sarapan
> foo
Perintah tidak dikenal
> keluar
```

Teks setelah tanda `>` adalah yang kamu ketik sendiri; sisanya dicetak program. Setelah `keluar` kamu kembali ke prompt Ubuntu.

### E2 — Coba sendiri

Jalankan lagi `uv run main.py`, lalu ketik `add` diikuti spasi saja, Enter. Harus muncul "Judul tidak boleh kosong". Ketik `list` sebelum menambah apa pun: tidak ada yang tampil, dan itu benar karena daftar baru kosong tiap program dijalankan.

**Kata baru:** `while True` (mengulang tanpa henti), `input` (menunggu ketikan), `break` (keluar dari perulangan), `if / elif / else` (memilih jalur), `strip` (membuang spasi di tepi).

### Titik cek E

- [ ] `add` menambah tugas, `list` menampilkannya bernomor
- [ ] Perintah asal-asalan menampilkan "Perintah tidak dikenal"
- [ ] `keluar` mengembalikanku ke prompt Ubuntu
- [ ] Aku tahu bahwa data hilang saat program ditutup (disimpan ke file di Hari 2)

---

## Bagian F — Menandai selesai dan statistik (15 menit)

Setelah bagian ini kamu bisa menandai tugas selesai dan melihat ringkasan. Ini versi akhir `main.py` Hari 1.

### F1 — Tambah dua fungsi dan dua perintah

**Folder:** `~/sakura-tasks`

**File:** `/home/nama/sakura-tasks/main.py`

Ketik dua fungsi baru di **antara** fungsi `tampilkan` dan baris `print("sakura-tasks...`. Lalu ubah baris `print` pembuka dan tambah dua cabang di dalam `while`. Paling aman: ganti seluruh isi file dengan versi lengkap di bawah.

**Isi lengkap main.py setelah bagian F:**

```python
tugas = []

def tambah(judul):
    judul = judul.strip()
    if judul == "":
        print("Judul tidak boleh kosong")
        return
    tugas.append({"judul": judul, "selesai": False})
    print(f"Ditambahkan: {judul}")

def tampilkan():
    for nomor, item in enumerate(tugas, start=1):
        tanda = "x" if item["selesai"] else " "
        print(f"{nomor}. [{tanda}] {item['judul']}")

def selesai(nomor):
    if nomor < 1 or nomor > len(tugas):
        print("Nomor tidak ada")
        return
    tugas[nomor - 1]["selesai"] = True
    print(f"Selesai: {tugas[nomor - 1]['judul']}")

def ringkasan():
    total = len(tugas)
    jumlah_selesai = 0
    for item in tugas:
        if item["selesai"]:
            jumlah_selesai += 1
    print(f"Total {total} | selesai {jumlah_selesai} | belum {total - jumlah_selesai}")

print("sakura-tasks. Perintah: add JUDUL, list, done NOMOR, stats, keluar")
while True:
    perintah = input("> ")
    if perintah == "keluar":
        break
    elif perintah == "list":
        tampilkan()
    elif perintah == "stats":
        ringkasan()
    elif perintah.startswith("add "):
        tambah(perintah[4:])
    elif perintah.startswith("done "):
        nomor = perintah[5:]
        if nomor.isdigit():
            selesai(int(nomor))
        else:
            print("Nomor harus angka")
    else:
        print("Perintah tidak dikenal")
```

Simpan dengan Ctrl+S.

**Jalankan di terminal:**

```text
uv run main.py
```

**Ketik di dalam program (setelah tanda >):**

```text
add bangun pagi
add sarapan
done 1
done 9
done x
list
stats
keluar
```

**Yang harus muncul di layar:**

```text
sakura-tasks. Perintah: add JUDUL, list, done NOMOR, stats, keluar
> add bangun pagi
Ditambahkan: bangun pagi
> add sarapan
Ditambahkan: sarapan
> done 1
Selesai: bangun pagi
> done 9
Nomor tidak ada
> done x
Nomor harus angka
> list
1. [x] bangun pagi
2. [ ] sarapan
> stats
Total 2 | selesai 1 | belum 1
> keluar
```

### F2 — Coba sendiri

Tambah tiga tugas, tandai dua selesai, jalankan `stats`. Angka harus cocok dengan `list`.

**Kata baru:** `return` (keluar dari fungsi lebih awal), `len` (jumlah isi daftar), `isdigit` (cek teks berisi angka saja), `int` (ubah teks jadi angka), `+= 1` (tambah satu).

### Titik cek F

- [ ] `done 1` mengubah `[ ]` jadi `[x]` di `list`
- [ ] `done 9` dan `done x` ditolak dengan pesan
- [ ] `stats` cocok dengan isi `list`
- [ ] Aku bisa menjelaskan kenapa `done 1` mengubah `tugas[0]` (nomor layar dikurangi 1)

---

## Bagian G — Simpan ke Git dan GitHub (15 menit)

Setelah bagian ini kodemu tersimpan sebagai commit dan ada di GitHub. Ini juga cara trainer melihat pekerjaanmu.

Semua perintah di bagian ini diketik di **terminal VS Code** (atau terminal Ubuntu) dengan prompt berakhir `~/sakura-tasks$`. Kalau terminalmu masih menjalankan program (tanda `>`), ketik `keluar` dulu.

Perintah `uv init` tadi sudah membuat repo Git di laptopmu, jadi tidak perlu `git init`. Satu proyek = satu repo = satu folder.

### G1 — Cek status

**Folder:** `~/sakura-tasks`

**Ketik:**

```text
git status
```

**Yang harus muncul di layar:** daftar file berwarna merah di bawah `Untracked files` atau `Changes not staged`, termasuk `main.py`. Artinya Git melihat file, tapi belum menyimpannya.

### G2 — Simpan sebagai commit

**Ketik, satu per satu:**

```text
git add .
```

```text
git commit -m "Hari 1: sakura-tasks interaktif"
```

**Yang harus muncul di layar:** baris yang mengandung `1 file changed` atau `N files changed`, dan nama commit tadi.

Kalau muncul pesan `Please tell me who you are`: kembali ke setup Git di Bagian A (user.name dan user.email), lalu ulangi `git commit`.

```text
git log --oneline
```

**Yang harus muncul:** satu baris berisi kode pendek dan "Hari 1: sakura-tasks interaktif". Tekan `q` bila layar menunggu.

### G3 — Buat repo di GitHub (di browser)

1. Buka github.com, login.
2. Klik tanda `+` kanan atas, pilih **New repository**.
3. Repository name: `sakura-tasks`.
4. Pilih **Private**.
5. **Jangan** centang Add a README, .gitignore, atau license.
6. Klik **Create repository**.
7. Buka **Settings**, **Collaborators**, **Add people**, lalu undang username GitHub trainer: `USERNAME-GITHUB-TRAINER`.

### G4 — Kirim kode ke GitHub

Ganti `USERNAMEKAMU` dengan username GitHub-mu, tanpa spasi dan tanpa tanda kurung.

**Ketik, satu per satu:**

```text
git branch -M main
```

```text
git remote add origin git@github.com:USERNAMEKAMU/sakura-tasks.git
```

```text
git push -u origin main
```

Bila ditanya `Are you sure you want to continue connecting`, ketik `yes` lalu Enter.

**Yang harus muncul di layar:** baris `Writing objects: 100%` dan `branch 'main' set up to track 'origin/main'`.

**Cek di browser:** muat ulang halaman repo. `main.py` harus terlihat.

### Titik cek G

- [ ] `git log --oneline` menampilkan commit Hari 1
- [ ] Repo `sakura-tasks` private ada di GitHub dan berisi `main.py`
- [ ] Trainer sudah diundang sebagai collaborator
- [ ] Aku tahu beda `git add` (pilih file), `git commit` (simpan di laptop), `git push` (kirim ke GitHub)

### Resep: satu proyek = satu repository

Pola ini dipakai untuk setiap proyek baru. Ganti `NAMA-PROYEK` dengan nama proyek dan `USERNAMEKAMU` dengan username GitHub-mu.

| Langkah | Ketik atau lakukan | Di mana |
| --- | --- | --- |
| 1. Buat proyek | `cd ~` lalu `uv init NAMA-PROYEK --python 3.12` | Terminal Ubuntu |
| 2. Masuk ke proyek | `cd NAMA-PROYEK` | Terminal Ubuntu |
| 3. Commit pertama | `git add .` lalu `git commit -m "Pesan awal"` | Terminal Ubuntu |
| 4. Buat repo kosong | New repository, nama sama persis `NAMA-PROYEK`, Private, tanpa README | Browser, GitHub |
| 5. Hubungkan dan kirim | `git branch -M main`, lalu `git remote add origin git@github.com:USERNAMEKAMU/NAMA-PROYEK.git`, lalu `git push -u origin main` | Terminal Ubuntu |

`uv init` sudah menjalankan `git init`, jadi jangan menjalankannya lagi dan jangan membuat repo di dalam repo lain. Setelah terhubung, setiap perubahan cukup `git add .`, `git commit -m "..."`, `git push`. Hari 2 melanjutkan proyek dan repo yang sama.

---

## Titik cek akhir Hari 1 dan jika ada masalah

### Target minimal Hari 1

- [ ] Proyek `sakura-tasks` ada di `~/` (bukan `/mnt/c/`)
- [ ] `uv run main.py` menjalankan program interaktif
- [ ] Perintah `add`, `list`, `done`, `stats`, `keluar` jalan
- [ ] Ada satu commit, dan repo private ada di GitHub

Belum semua tercentang? Tidak masalah. Kerjakan terus sesuai kecepatanmu, dan kabari trainer di grup dengan menyebut **bagian mana** (contoh: "P08 stuck di E1") serta tempel pesan error di terminal.

### Masalah yang sering muncul

| Yang kamu lihat | Penyebab | Yang diketik / dilakukan |
| --- | --- | --- |
| `command not found: uv` | uv belum terpasang atau terminal belum dimuat ulang | Tutup terminal, buka lagi, coba `uv --version`. Kalau tetap gagal, kabari trainer |
| `No such file or directory: main.py` | Terminal ada di folder yang salah | `cd ~/sakura-tasks`, lalu `ls` harus menampilkan `main.py` |
| `IndentationError` atau `unexpected indent` | Jorokan tidak 4 spasi, atau campur Tab dan spasi | Cek baris yang disebut error, rapikan jadi 4 atau 8 spasi |
| `SyntaxError` | Titik dua, tanda kurung, atau tanda kutip kurang | Lihat baris yang ditunjuk panah `^`, bandingkan dengan lembar ini huruf demi huruf |
| `NameError: name 'xxx' is not defined` | Salah ketik nama, atau fungsi dipanggil sebelum dibuat | Cocokkan ejaan dengan lembar ini; fungsi harus ditulis di atas pemanggilnya |
| Program tidak menanggapi apa pun | Program menunggu input di tanda `>` | Ketik perintah, atau `keluar` |
| `Permission denied (publickey)` saat `git push` | Kunci SSH belum terdaftar di GitHub | Kabari trainer, tempel pesan lengkapnya |
| `Author identity unknown` saat commit | user.name dan user.email belum diatur | Ulangi setup Git di Bagian A |
| Pesan `remote origin already exists` | Perintah `git remote add` sudah pernah diketik | `git remote set-url origin git@github.com:USERNAMEKAMU/sakura-tasks.git` |

### Jalur kejar

Kalau tertinggal beberapa bagian, tidak perlu mengetik ulang semuanya. Salin **Isi lengkap main.py setelah bagian F** ke `main.py` (Ctrl+A, Delete, tempel, Ctrl+S), jalankan `uv run main.py`, lalu lanjut ke bagian berikutnya.

Hari 2 dimulai dari file ini.
