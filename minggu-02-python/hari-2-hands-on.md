# Hari 2 — Hands-on: modul dan OOP di sakura-tasks

Hari ini kamu merapikan program Hari 1 dalam dua tahap: **dipecah jadi modul**, lalu **diubah jadi class (OOP)**. Perilaku program tidak berubah. Yang berubah adalah cara kodenya disusun. Aturan mainnya sama seperti Hari 1: ikuti langkah berurutan, ketik persis, cocokkan hasilmu dengan **Yang harus muncul di layar**. Penjelasan disampaikan trainer sambil mengetik.

## Tujuan hari ini

Di akhir Hari 2, **semua peserta punya hasil yang sama**: `sakura-tasks` yang tersusun dari dua file (`main.py` dan `tugas.py`), memakai class `Tugas` dan `PengelolaTugas`, dan tersimpan di repo GitHub yang sama dengan Hari 1.

### Hasil akhir yang dikejar

```text
sakura-tasks-p08/
  main.py            menerima perintah, memanggil PengelolaTugas
  tugas.py           class Tugas dan PengelolaTugas (modul)
  pyproject.toml     identitas proyek
```

Program dijalankan sama seperti kemarin, dan tampilannya **tidak berubah**:

```text
uv run main.py
```

Data tugas masih hilang saat program ditutup. Itu normal. Penyimpanan data punya materinya sendiri (database), jadi tidak dikerjakan hari ini.

## Persiapan sebelum mulai

- [ ] Proyek `~/sakura-tasks-p08` dari Hari 1 ada, dan `uv run main.py` jalan
- [ ] Aplikasi **Ubuntu** terbuka dari menu Windows (bukan PowerShell)
- [ ] VS Code bisa dibuka dari folder proyek dengan `code .` (pojok kiri bawah tertulis **WSL: Ubuntu**)
- [ ] Repo `sakura-tasks-p08` dari Hari 1 sudah ada di GitHub (organization `bootcamp-seti-1`)
- [ ] Aku tahu ID pesertaku (P01 sampai P25)

Belum selesai Hari 1? Buka lembar Hari 1, salin **Isi lengkap main.py setelah bagian F** ke `main.py`, jalankan, dan mulai dari Bagian A di bawah.

## Peta Hari 2 (±120 menit)

| Bagian | Isi | Menit | Hasilnya |
| --- | --- | --- | --- |
| A | Pemanasan | 8 | Titik awal sama untuk semua |
| B | Modul | 25 | Fungsi pindah ke `tugas.py`, `main.py` memanggilnya |
| C | OOP 1: class `Tugas` | 28 | Satu tugas jadi objek |
| D | OOP 2: class `PengelolaTugas` | 25 | Daftar dan fungsi jadi satu objek, variabel global hilang |
| E | Perbandingan prosedural dan OOP | 8 | Tahu kapan memakai yang mana |
| F | Latihan: perintah `hapus` | 8 | Method baru buatanmu sendiri |
| G | Git dan GitHub | 8 | Commit kedua di repo yang sama |
| H | Kuis | 10 | 10 soal pilihan ganda |

Label **Folder**, **File**, **Ketik**, **Jalankan**, dan **Yang harus muncul di layar** artinya sama dengan Hari 1. Ada satu tambahan:

| Tanda | Artinya |
| --- | --- |
| `>` | Perintah yang diketik **di dalam program sakura-tasks** (seperti Hari 1) |
| `>>>` | Prompt **Python interaktif** (ruang mencoba kode baris demi baris). Tanda `>>>` dicetak Python sendiri, jadi **tidak diketik**. Kotak **Ketik** hanya berisi baris yang kamu ketik |

---

## Bagian A — Pemanasan (8 menit)

Setelah bagian ini kamu yakin proyek Hari 1 siap dilanjutkan.

### A1 — Masuk ke proyek dan cek kondisinya

**Folder:** `~`

**Ketik** (satu baris per Enter):

```text
cd ~/sakura-tasks-p08
git status
```

Ganti `p08` dengan ID pesertamu (huruf kecil).

**Yang harus muncul di layar:**

```text
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

Artinya semua pekerjaan Hari 1 sudah tersimpan. Kalau ada daftar file merah, commit dulu dengan `git add .` lalu `git commit -m "Rapikan Hari 1"`.

### A2 — Jalankan program Hari 1

**Folder:** `~/sakura-tasks-p08`

**Jalankan:**

```text
uv run main.py
```

**Ketik di dalam program (setelah tanda >):**

```text
add bangun pagi
list
keluar
```

**Yang harus muncul di layar:**

```text
sakura-tasks. Perintah: add JUDUL, list, done NOMOR, stats, keluar
> add bangun pagi
Ditambahkan: bangun pagi
> list
1. [ ] bangun pagi
> keluar
```

### A3 — Lihat masalahnya

Buka `main.py` di VS Code (`code .` kalau belum terbuka). Perhatikan tiga hal:

1. Semuanya ada di **satu file**: daftar tugas, fungsi, dan loop perintah.
2. Semua fungsi memakai satu variabel **global** `tugas`. Siapa pun di file ini bisa mengubahnya.
3. Satu tugas hanyalah dictionary `{"judul": ..., "selesai": ...}`. Tidak ada yang menjaga isinya benar.

Hari ini kita rapikan tiga hal itu satu per satu.

---

## Bagian B — Modul: pisahkan kode ke file sendiri (25 menit)

> **Penjelasan singkat (5 menit)**
>
> - **Modul** adalah file `.py` biasa yang isinya bisa dipakai file lain. Nama modulnya sama dengan nama file tanpa `.py`: file `tugas.py` jadi modul `tugas`.
> - File lain memakainya dengan `import tugas`, lalu memanggil isinya dengan titik: `tugas.tambah("sarapan")`.
> - Kenapa dipisah: tiap file punya satu tugas. `tugas.py` mengurus logika tugas, `main.py` hanya menerima perintah. File jadi pendek, mudah dicari, dan bisa dipakai ulang.
> - Ada dua bentuk import: `import tugas` (panggil dengan `tugas.nama`) dan `from tugas import nama` (panggil langsung `nama`). Hari ini keduanya dipakai.

Setelah bagian ini programmu tersusun dari dua file dan jalan persis seperti Hari 1.

### B1 — Buat file tugas.py

**Di VS Code** (proyek `sakura-tasks-p08` sudah terbuka dari Hari 1):

1. Di panel kiri, klik ikon **New File** (kertas dengan tanda plus), atau klik kanan area kosong di panel kiri lalu pilih **New File**.
2. Ketik nama `tugas.py`, lalu tekan Enter.

File kosong `tugas.py` muncul di panel kiri, sejajar dengan `main.py`.

### B2 — Isi tugas.py dengan fungsi-fungsi dari main.py

**File:** `/home/nama/sakura-tasks-p08/tugas.py` (Baru)

Buka `tugas.py` di VS Code dan ketik isi berikut. Isinya sama dengan fungsi di `main.py` Hari 1, tanpa loop perintahnya.

**Isi lengkap tugas.py setelah bagian B:**

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
```

Simpan dengan Ctrl+S.

### B3 — Ganti isi main.py

**File:** `/home/nama/sakura-tasks-p08/main.py` (sudah ada; ganti seluruh isinya: Ctrl+A, Delete)

`main.py` sekarang hanya memuat loop perintah. Semua panggilan fungsi memakai awalan `tugas.`.

**Isi lengkap main.py setelah bagian B:**

```python
import tugas

print("sakura-tasks. Perintah: add JUDUL, list, done NOMOR, stats, keluar")
while True:
    perintah = input("> ")
    if perintah == "keluar":
        break
    elif perintah == "list":
        tugas.tampilkan()
    elif perintah == "stats":
        tugas.ringkasan()
    elif perintah.startswith("add "):
        tugas.tambah(perintah[4:])
    elif perintah.startswith("done "):
        nomor = perintah[5:]
        if nomor.isdigit():
            tugas.selesai(int(nomor))
        else:
            print("Nomor harus angka")
    else:
        print("Perintah tidak dikenal")
```

Simpan dengan Ctrl+S.

### B4 — Jalankan

**Folder:** `~/sakura-tasks-p08`

**Jalankan:**

```text
uv run main.py
```

**Ketik di dalam program (setelah tanda >):**

```text
add bangun pagi
add sarapan
done 1
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
> list
1. [x] bangun pagi
2. [ ] sarapan
> stats
Total 2 | selesai 1 | belum 1
> keluar
```

Hasilnya sama persis dengan Hari 1. Folder `__pycache__` mungkin muncul di proyekmu. Itu normal dan sudah diabaikan oleh Git.

### B5 — Coba sendiri

Di `tugas.py`, ubah tulisan `Ditambahkan:` di fungsi `tambah` menjadi `Tugas baru:`. Simpan, lalu jalankan lagi `uv run main.py` dan ketik `add tes`. Harus muncul `Tugas baru: tes`, padahal kamu **tidak menyentuh `main.py`**. Itulah gunanya memisahkan kode.

Setelah itu kembalikan lagi menjadi `Ditambahkan:`.

**Kata baru:** modul, `import`, `tugas.tambah(...)` (isi modul dipanggil dengan titik).

---

## Bagian C — OOP 1: class Tugas (28 menit)

> **Penjelasan singkat (12 menit)**
>
> - Bayangkan **formulir tugas**. Formulir kosong yang sama dicetak untuk semua orang itu **class**. Formulir yang sudah diisi (judul "bangun pagi", belum selesai) itu **objek**. Satu class bisa menghasilkan banyak objek, dan tiap objek punya isinya sendiri.
> - Di Hari 1 satu tugas adalah dictionary: `{"judul": ..., "selesai": ...}`. Sekarang satu tugas adalah **objek `Tugas`** yang membawa datanya (atribut) **dan** kemampuannya (method).
> - `class Tugas:` membuat cetakannya. `Tugas("sarapan")` membuat satu objek dari cetakan itu.
> - `__init__` adalah method yang **dijalankan otomatis** saat objek dibuat. Tugasnya mengisi data awal.
> - `self` berarti **objek yang sedang dipakai**. Saat kamu menulis `t.tandai_selesai()`, Python mengirim `t` sebagai `self`. Karena itu method selalu menulis `self` di parameter pertamanya.

| Kode | Artinya |
| --- | --- |
| `class Tugas:` | Membuat cetakan bernama Tugas |
| `Tugas("sarapan")` | Membuat satu objek dari cetakan itu (menjalankan `__init__`) |
| `self.judul` | Atribut `judul` milik objek ini |
| `def tandai_selesai(self):` | Method: fungsi yang melekat pada objek |
| `__str__` | Method khusus: menentukan tulisan objek saat di-`print` |

### OOP dalam kehidupan sehari-hari

Bayangkan kamu mengelola **papan sticky note** di kantor Sakura Soft. Setiap tugas ditulis di satu sticky note.

| Di dunia nyata | Di kode |
| --- | --- |
| Cetakan sticky note: kertas berformat dengan kolom judul dan kotak centang | class `Tugas` |
| Satu sticky note yang sudah ditulisi "sarapan" | Objek `Tugas("sarapan")` |
| Tulisan judul dan centang di note itu | Atribut `judul` dan `selesai` |
| Aksi mencentang note | Method `tandai_selesai()` |
| Saat note baru ditulis: judul diisi, kotak centang dibiarkan kosong | `__init__` |
| "Note yang sedang kamu pegang" | `self` |
| Papan yang menyimpan banyak note dan tahu cara menambah, menampilkan, mencentang, dan menghitungnya | class `PengelolaTugas` (Bagian D) |
| Tumpukan note di papan itu | `self.daftar` |

**`self` itu seperti kata "saya".** Kalau Budi bilang "saya lapar", yang lapar Budi. Kalau Ani mengucapkan kalimat yang sama, yang lapar Ani. Kata "saya" selalu menunjuk siapa yang sedang bicara. Begitu juga `self`: di dalam method, `self` menunjuk objek yang sedang memanggilnya. Itu sebabnya `a.tandai_selesai()` hanya mencentang note `a`, bukan note `b`.

**Kenapa data dan kemampuan disatukan?** Ambil contoh rekening tabungan. Saldo (data) dan aturan "tidak boleh menarik lebih dari saldo" (kemampuan) sebaiknya berada di tempat yang sama, supaya aturannya tidak terlewat. Contoh ini **dibaca saja, tidak diketik**:

```python
class Rekening:
    def __init__(self, pemilik, saldo):
        self.pemilik = pemilik
        self.saldo = saldo

    def tarik(self, jumlah):
        if jumlah > self.saldo:
            print("Saldo tidak cukup")
            return
        self.saldo -= jumlah
        print(f"Saldo sekarang {self.saldo}")


budi = Rekening("Budi", 100000)
ani = Rekening("Ani", 500000)
budi.tarik(150000)
ani.tarik(150000)
```

Hasilnya:

```text
Saldo tidak cukup
Saldo sekarang 350000
```

Rekening Budi (saldo 100000) menolak penarikan 150000, sedangkan rekening Ani (saldo 500000) berhasil. Dua objek, dua saldo, satu aturan yang ditulis sekali di dalam class. Di gaya prosedural, saldo dan fungsi tarik berdiri terpisah, jadi lebih mudah ada kode lain yang mengubah saldo tanpa melewati aturan itu.

### Apakah OOP harus Java?

**Tidak.** OOP adalah **cara menyusun program**, bukan fitur milik satu bahasa. Banyak bahasa mendukungnya. Konsepnya sama (class, objek, atribut, method), yang berbeda hanya cara menulisnya.

| Bahasa | Mendukung OOP? | Catatan |
| --- | --- | --- |
| Python | Ya | Boleh prosedural atau OOP, bebas dicampur (seperti Hari 1 dan Hari 2) |
| Java | Ya | Dirancang berorientasi objek, hampir semua kode ditulis di dalam class |
| C# | Ya | Mirip Java |
| JavaScript / TypeScript | Ya | Punya `class`, tapi bisa juga ditulis tanpa class |
| PHP, C++, Kotlin, Swift, Ruby | Ya | |
| C | Tidak punya class | Bahasa prosedural: program ditulis dengan fungsi dan `struct` |

Class `Tugas` yang sama dalam tiga bahasa. **Dibaca saja, tidak diketik:**

```python
# Python
class Tugas:
    def __init__(self, judul):
        self.judul = judul
        self.selesai = False

    def tandai_selesai(self):
        self.selesai = True
```

```java
// Java
class Tugas {
    String judul;
    boolean selesai = false;

    Tugas(String judul) {
        this.judul = judul;
    }

    void tandaiSelesai() {
        this.selesai = true;
    }
}
```

```javascript
// JavaScript
class Tugas {
  constructor(judul) {
    this.judul = judul;
    this.selesai = false;
  }

  tandaiSelesai() {
    this.selesai = true;
  }
}
```

Perhatikan: kerangkanya sama (class, data awal, satu method). Yang berbeda hanya ejaan: Python memakai `__init__` dan `self` yang ditulis jelas di parameter, Java dan JavaScript memakai `constructor` (di Java, nama class) dan `this`, dan Java menulis tipe data seperti `String` dan `boolean`. Setelah paham di Python, berpindah ke bahasa lain sebagian besar tinggal belajar ejaannya.

Setelah bagian ini satu tugas adalah objek, dan program tetap berjalan seperti sebelumnya.

### C1 — Ganti isi tugas.py

**Folder:** `~/sakura-tasks-p08`

**File:** `/home/nama/sakura-tasks-p08/tugas.py` (ganti seluruh isinya: Ctrl+A, Delete)

Class `Tugas` ada di bagian atas. Fungsi-fungsinya masih ada di bawah, tetapi sekarang menyimpan objek `Tugas` di daftar bernama `daftar`.

**Isi lengkap tugas.py setelah bagian C:**

```python
class Tugas:
    def __init__(self, judul):
        self.judul = judul
        self.selesai = False

    def tandai_selesai(self):
        self.selesai = True

    def __str__(self):
        tanda = "x" if self.selesai else " "
        return f"[{tanda}] {self.judul}"


daftar = []

def tambah(judul):
    judul = judul.strip()
    if judul == "":
        print("Judul tidak boleh kosong")
        return
    daftar.append(Tugas(judul))
    print(f"Ditambahkan: {judul}")

def tampilkan():
    for nomor, item in enumerate(daftar, start=1):
        print(f"{nomor}. {item}")

def selesai(nomor):
    if nomor < 1 or nomor > len(daftar):
        print("Nomor tidak ada")
        return
    item = daftar[nomor - 1]
    item.tandai_selesai()
    print(f"Selesai: {item.judul}")

def ringkasan():
    total = len(daftar)
    jumlah_selesai = 0
    for item in daftar:
        if item.selesai:
            jumlah_selesai += 1
    print(f"Total {total} | selesai {jumlah_selesai} | belum {total - jumlah_selesai}")
```

Method di dalam class menjorok 4 spasi dari `class`, dan isi method menjorok 8 spasi. Dua baris kosong sebelum `daftar = []` hanya untuk kerapian. Simpan dengan Ctrl+S.

`main.py` **tidak diubah**. Ia tetap memanggil `tugas.tambah(...)`, `tugas.tampilkan()`, dan seterusnya.

### C2 — Jalankan program

**Folder:** `~/sakura-tasks-p08`

**Jalankan:**

```text
uv run main.py
```

Ketik perintah yang sama seperti di B4 (`add bangun pagi`, `add sarapan`, `done 1`, `list`, `stats`, `keluar`).

**Yang harus muncul di layar:** sama persis dengan B4. Tampilannya tidak berubah. Yang berubah hanya isi di balik layar: satu tugas sekarang adalah objek.

### C3 — Bermain dengan objek di Python interaktif

**Folder:** `~/sakura-tasks-p08`

Python interaktif adalah ruang untuk mencoba kode baris demi baris. Masuk dengan:

```text
uv run python
```

Beberapa baris tentang versi Python muncul, lalu prompt berubah menjadi `>>>`. Ketik baris berikut **satu per satu**, tekan Enter setiap baris.

**Ketik:**

```text
from tugas import Tugas
t = Tugas("bangun pagi")
print(t)
t.tandai_selesai()
print(t)
a = Tugas("sarapan")
b = Tugas("mandi")
a.tandai_selesai()
print(a)
print(b)
exit()
```

**Yang harus muncul di layar:**

```text
>>> from tugas import Tugas
>>> t = Tugas("bangun pagi")
>>> print(t)
[ ] bangun pagi
>>> t.tandai_selesai()
>>> print(t)
[x] bangun pagi
>>> a = Tugas("sarapan")
>>> b = Tugas("mandi")
>>> a.tandai_selesai()
>>> print(a)
[x] sarapan
>>> print(b)
[ ] mandi
>>> exit()
```

Perhatikan: `a` sudah ditandai selesai, tetapi `b` tidak ikut berubah. Dua objek dari class yang sama punya data **sendiri-sendiri**. Itulah fungsi `self`.

### C4 — Coba sendiri

Masuk lagi dengan `uv run python`, lalu buat objek ketiga dengan judulmu sendiri, misalnya `c = Tugas("olahraga")`. Ketik `print(c.judul)` dan `print(c.selesai)`. Harus muncul judulmu, lalu `False`. Keluar dengan `exit()`.

**Kata baru:** class, objek, atribut, method, `__init__`, `self`, `__str__`.

---

## Bagian D — OOP 2: class PengelolaTugas (25 menit)

> **Penjelasan singkat (5 menit)**
>
> - Sekarang tiap tugas sudah objek, tetapi **daftarnya** (`daftar`) masih variabel global dan fungsinya masih berdiri sendiri.
> - Kita bungkus semuanya ke objek baru: **`PengelolaTugas`**. Ia memegang daftar tugas dan tahu cara menambah, menampilkan, menandai selesai, dan meringkas.
> - Fungsi `tambah`, `tampilkan`, `selesai`, `ringkasan` menjadi **method** (tambah parameter `self`). Variabel global `daftar` menjadi atribut `self.daftar`.
> - Hasilnya: tidak ada lagi variabel global yang bisa diubah dari mana saja, dan kamu bisa punya **lebih dari satu** pengelola yang saling terpisah.

Setelah bagian ini variabel global hilang dan `main.py` bekerja lewat satu objek pengelola.

### D1 — Ganti isi tugas.py

**Folder:** `~/sakura-tasks-p08`

**File:** `/home/nama/sakura-tasks-p08/tugas.py` (ganti seluruh isinya: Ctrl+A, Delete)

Class `Tugas` **tetap sama**. Fungsi-fungsi di bawahnya diganti oleh class `PengelolaTugas`.

**Isi lengkap tugas.py setelah bagian D:**

```python
class Tugas:
    def __init__(self, judul):
        self.judul = judul
        self.selesai = False

    def tandai_selesai(self):
        self.selesai = True

    def __str__(self):
        tanda = "x" if self.selesai else " "
        return f"[{tanda}] {self.judul}"


class PengelolaTugas:
    def __init__(self):
        self.daftar = []

    def tambah(self, judul):
        judul = judul.strip()
        if judul == "":
            print("Judul tidak boleh kosong")
            return
        self.daftar.append(Tugas(judul))
        print(f"Ditambahkan: {judul}")

    def tampilkan(self):
        for nomor, item in enumerate(self.daftar, start=1):
            print(f"{nomor}. {item}")

    def selesai(self, nomor):
        if nomor < 1 or nomor > len(self.daftar):
            print("Nomor tidak ada")
            return
        item = self.daftar[nomor - 1]
        item.tandai_selesai()
        print(f"Selesai: {item.judul}")

    def ringkasan(self):
        total = len(self.daftar)
        jumlah_selesai = 0
        for item in self.daftar:
            if item.selesai:
                jumlah_selesai += 1
        print(f"Total {total} | selesai {jumlah_selesai} | belum {total - jumlah_selesai}")
```

Method di `PengelolaTugas` menjorok 4 spasi, isinya 8 spasi, dan isi `for` 12 spasi. Simpan dengan Ctrl+S.

### D2 — Ganti isi main.py

**File:** `/home/nama/sakura-tasks-p08/main.py` (ganti seluruh isinya: Ctrl+A, Delete)

Sekarang `main.py` membuat **satu objek pengelola**, lalu semua perintah dikirim ke objek itu.

**Isi lengkap main.py setelah bagian D:**

```python
from tugas import PengelolaTugas

pengelola = PengelolaTugas()

print("sakura-tasks. Perintah: add JUDUL, list, done NOMOR, stats, keluar")
while True:
    perintah = input("> ")
    if perintah == "keluar":
        break
    elif perintah == "list":
        pengelola.tampilkan()
    elif perintah == "stats":
        pengelola.ringkasan()
    elif perintah.startswith("add "):
        pengelola.tambah(perintah[4:])
    elif perintah.startswith("done "):
        nomor = perintah[5:]
        if nomor.isdigit():
            pengelola.selesai(int(nomor))
        else:
            print("Nomor harus angka")
    else:
        print("Perintah tidak dikenal")
```

Perhatikan baris `from tugas import PengelolaTugas`. Karena memakai bentuk `from ... import`, class dipanggil langsung tanpa awalan `tugas.`. Simpan dengan Ctrl+S.

### D3 — Jalankan program

**Folder:** `~/sakura-tasks-p08`

**Jalankan:**

```text
uv run main.py
```

Ketik perintah yang sama seperti di B4 (`add bangun pagi`, `add sarapan`, `done 1`, `list`, `stats`, `keluar`).

**Yang harus muncul di layar:** sama persis dengan B4.

### D4 — Dua pengelola yang saling terpisah

**Folder:** `~/sakura-tasks-p08`

**Jalankan:**

```text
uv run python
```

**Ketik** (satu per satu, tekan Enter setiap baris):

```text
from tugas import PengelolaTugas
a = PengelolaTugas()
b = PengelolaTugas()
a.tambah("bangun pagi")
a.tampilkan()
b.tampilkan()
exit()
```

**Yang harus muncul di layar:**

```text
>>> from tugas import PengelolaTugas
>>> a = PengelolaTugas()
>>> b = PengelolaTugas()
>>> a.tambah("bangun pagi")
Ditambahkan: bangun pagi
>>> a.tampilkan()
1. [ ] bangun pagi
>>> b.tampilkan()
>>> exit()
```

Perhatikan `b.tampilkan()`: **tidak ada yang tampil**, karena daftar `b` memang kosong. Dengan variabel global di Hari 1 hal ini tidak mungkin: hanya ada satu daftar untuk seluruh program.

### D5 — Coba sendiri

Masuk lagi dengan `uv run python`. Buat dua pengelola, tambahkan tugas yang **berbeda** ke masing-masing (`a.tambah("...")`, `b.tambah("...")`), lalu jalankan `a.tampilkan()` dan `b.tampilkan()`. Tiap daftar hanya berisi tugasnya sendiri.

**Kata baru:** method, `self.daftar` (atribut milik objek), `from ... import`.

---

## Bagian E — Prosedural vs OOP (8 menit)

Bagian ini dibaca dan didiskusikan, tidak ada yang diketik.

Kamu baru saja menulis program yang **sama** dengan dua gaya. Hari 1 memakai gaya **prosedural** (sering juga disebut terstruktur): program disusun sebagai urutan langkah berupa fungsi. Hari 2 memakai **OOP** (Object-Oriented Programming): program disusun sebagai objek yang membungkus data bersama fungsi miliknya.

### Perbandingan kode yang sama

Menandai tugas selesai, dulu dan sekarang:

```python
# Prosedural (Hari 1): data dan fungsi terpisah
tugas = []

def selesai(nomor):
    tugas[nomor - 1]["selesai"] = True
```

```python
# OOP (sekarang): data dan fungsi dibungkus bersama
class Tugas:
    def tandai_selesai(self):
        self.selesai = True
```

### Tabel perbandingan

| Hal | Prosedural | OOP |
| --- | --- | --- |
| Cara berpikir | Urutan langkah (fungsi) | Benda (objek) yang punya data dan kemampuan |
| Data | Terpisah dari fungsi, sering global (`tugas` di Hari 1) | Dibungkus bersama method (`self.daftar`) |
| Contoh di sakura-tasks | List dictionary dan fungsi (Hari 1) | `Tugas` dan `PengelolaTugas` (Hari 2) |
| Kelebihan | Sederhana dan cepat ditulis untuk program kecil | Rapi saat program membesar, data lebih terjaga, mudah dikembangkan |
| Kekurangan | Makin besar makin kusut, banyak variabel global | Kode awal lebih banyak dan banyak istilah baru |
| Cocok untuk | Skrip pendek, sekali pakai | Aplikasi dengan banyak entitas (tugas, pengguna, pesanan) |

Keduanya bukan soal benar atau salah. Python mendukung dua-duanya, dan program nyata sering memakai campuran.

### Diskusikan dengan teman sebelahmu (3 menit)

1. Di Hari 1, bagaimana kalau kita butuh **dua** daftar tugas, misalnya untuk dua orang? Apa masalahnya dengan variabel global `tugas`?
2. Kapan kamu **tetap memilih** gaya prosedural, walau sudah tahu OOP?

> **Sekilas tentang pewarisan (inheritance).** Class baru bisa mengambil semua atribut dan method dari class lama, lalu menambah atau mengubah sebagian. Contoh: `TugasPrioritas` bisa mewarisi `Tugas` dan hanya menambahkan tanda khusus. Ini **tidak dikerjakan** hari ini. Cukup tahu bahwa istilahnya ada.

---

## Bagian F — Latihan: perintah hapus (8 menit)

Kerjakan sendiri, tanpa contoh kode. Gunakan yang baru kamu pelajari.

**Tujuannya:** menambah perintah `hapus NOMOR` yang menghapus tugas dari daftar.

**Folder:** `~/sakura-tasks-p08`

**Langkah:**

1. Di `tugas.py`, tambah method baru **`hapus(self, nomor)`** di dalam class `PengelolaTugas` (sejajar dengan `ringkasan`). Ia harus:
   - menolak nomor di luar daftar dengan pesan `Nomor tidak ada` (mirip method `selesai`),
   - kalau nomor benar, menghapus tugas itu dan menampilkan `Dihapus: JUDUL`.
2. Di `main.py`, tambah cabang `elif perintah.startswith("hapus "):` **sebelum** baris `else`. Cabangnya mirip perintah `done`: cek dulu angka atau bukan dengan `isdigit()`.
3. Jalankan `uv run main.py` dan cocokkan hasilnya dengan di bawah.

**Petunjuk:** list punya method `pop(indeks)` yang menghapus isi pada urutan tertentu dan mengembalikan isinya. Ingat, nomor di layar dikurangi 1 untuk menjadi urutan di list.

**Ketik di dalam program (setelah tanda >):**

```text
add a
add b
hapus 1
list
hapus 9
keluar
```

**Yang harus muncul di layar** (kalimat pembukanya boleh tetap seperti sebelumnya):

```text
> add a
Ditambahkan: a
> add b
Ditambahkan: b
> hapus 1
Dihapus: a
> list
1. [ ] b
> hapus 9
Nomor tidak ada
> keluar
```

Selesai lebih cepat? Ubah kalimat pembuka di `main.py` supaya `hapus NOMOR` ikut tertulis.

---

## Bagian G — Simpan ke Git dan GitHub (8 menit)

Ini commit kedua di repo yang sama dengan Hari 1. Semua perintah diketik di terminal dengan prompt berakhir `~/sakura-tasks-p08$`. Kalau terminalmu masih menjalankan program (tanda `>`), ketik `keluar` dulu.

### G1 — Cek status

**Folder:** `~/sakura-tasks-p08`

**Ketik:**

```text
git status
```

**Yang harus muncul di layar:** `main.py` tertulis `modified` (merah), dan `tugas.py` ada di bawah `Untracked files`. Artinya Git melihat perubahan, tapi belum menyimpannya.

### G2 — Commit dan push

**Ketik, satu per satu:**

```text
git add .
```

```text
git commit -m "Hari 2: modul dan OOP"
```

```text
git push
```

**Yang harus muncul di layar:** baris yang mengandung `2 files changed` dan nama commit, lalu `Writing objects: 100%`. Tidak perlu `-u` lagi, karena sudah diatur di Hari 1.

```text
git log --oneline
```

**Yang harus muncul:** dua baris, commit Hari 2 di atas dan commit Hari 1 di bawah. Kode pendek di depannya berbeda di tiap komputer. Tekan `q` bila layar menunggu.

```text
a1b2c3d Hari 2: modul dan OOP
e4f5a6b Hari 1: sakura-tasks interaktif
```

**Cek di browser:** muat ulang halaman repo `bootcamp-seti-1 / sakura-tasks-p08`. File `tugas.py` harus terlihat.

---

## Bagian H — Kuis (10 menit)

Kerjakan sendiri tanpa membuka lembar ini. Pilih satu jawaban (A sampai D) untuk tiap soal. Jawabanmu dikumpulkan lewat Google Form: https://forms.gle/hMwNCVotRWcPDZTV9

Di formulir itu, isi **ID pesertamu** (contoh: P08), bukan nama.

**Soal 1.** Kamu punya file `tugas.py` berisi fungsi `tambah`. Supaya `main.py` bisa memanggil `tugas.tambah("sarapan")`, baris yang dipakai di `main.py` adalah …

- A. `include tugas`
- B. `import tugas`
- C. `open("tugas.py")`
- D. `def tugas():`

**Soal 2.** Hubungan class dan objek yang benar adalah …

- A. Class dan objek adalah dua nama untuk hal yang sama
- B. Objek adalah cetakan, class adalah hasil cetakannya
- C. Class adalah cetakan, objek adalah hasil cetakannya
- D. Class hanya untuk angka, objek hanya untuk teks

**Soal 3.** Pada `def tandai_selesai(self):`, kata `self` berarti …

- A. Objek yang sedang memanggil method itu
- B. Nama file tempat class berada
- C. Kata kunci untuk keluar dari method
- D. Judul tugas

**Soal 4.** Method `__init__` dijalankan ketika …

- A. Program ditutup
- B. Method lain selesai dijalankan
- C. `print` dipanggil
- D. Objek baru dibuat, misalnya `Tugas("mandi")`

**Soal 5.** Apa yang tampil dari kode ini? (class `Tugas` seperti di Bagian C)

```python
a = Tugas("mandi")
b = Tugas("makan")
a.tandai_selesai()
print(a)
print(b)
```

- A. `[x] mandi` lalu `[x] makan`
- B. `[x] mandi` lalu `[ ] makan`
- C. `[ ] mandi` lalu `[ ] makan`
- D. Error

**Soal 6.** Setelah menulis `from tugas import PengelolaTugas` di `main.py`, cara membuat objek pengelola adalah …

- A. `tugas.PengelolaTugas()`
- B. `new PengelolaTugas()`
- C. `import PengelolaTugas()`
- D. `PengelolaTugas()`

**Soal 7.** Pernyataan yang menggambarkan pemrograman **prosedural** adalah …

- A. Program disusun sebagai urutan langkah (fungsi) yang memproses data yang terpisah dari fungsi itu
- B. Data dan fungsi selalu dibungkus bersama di dalam class
- C. Fungsi tidak boleh dipakai sama sekali
- D. Hanya bisa dipakai di bahasa Java

**Soal 8.** Situasi yang paling cocok memakai OOP adalah …

- A. Skrip 15 baris yang dijalankan sekali lalu dibuang
- B. Menghitung 2 + 2
- C. Mencetak satu kalimat ke layar
- D. Aplikasi dengan banyak entitas yang masing-masing punya data dan perilakunya sendiri, seperti tugas, pengguna, dan pesanan

**Soal 9.** Pernyataan yang benar tentang OOP dan bahasa pemrograman adalah …

- A. OOP adalah cara menyusun program yang bisa dipakai di banyak bahasa, misalnya Python, Java, JavaScript, dan C#
- B. OOP hanya bisa dipakai di Java
- C. Python tidak mendukung OOP
- D. OOP wajib memakai kata `self` di semua bahasa

**Soal 10.** Keuntungan memakai class `PengelolaTugas` dibanding satu variabel global `daftar` adalah …

- A. Program otomatis berjalan lebih cepat
- B. Data tugas otomatis tersimpan ke file
- C. Bisa punya beberapa pengelola yang masing-masing punya daftar sendiri
- D. Tidak perlu lagi memakai `self`

---

## Jika ada masalah

Kabari trainer di grup dengan menyebut **bagian mana** (contoh: "P08 stuck di C1") serta tempel pesan error di terminal.

### Masalah yang sering muncul

| Yang kamu lihat | Penyebab | Yang diketik / dilakukan |
| --- | --- | --- |
| `ModuleNotFoundError: No module named 'tugas'` | Terminal ada di folder yang salah, atau file `tugas.py` belum dibuat atau salah nama | `cd ~/sakura-tasks-p08`, lalu `ls` harus menampilkan `tugas.py` (huruf kecil semua) |
| `ImportError: cannot import name 'PengelolaTugas' from 'tugas'` | Ejaan nama class beda, atau `tugas.py` belum disimpan, atau masih versi Bagian C | Cocokkan ejaan, simpan dengan Ctrl+S, pastikan `tugas.py` versi Bagian D |
| `AttributeError: module 'tugas' has no attribute 'tambah'` | `tugas.py` sudah versi D (class), tetapi `main.py` masih versi B | Ganti `main.py` dengan versi lengkap Bagian D |
| `TypeError: PengelolaTugas.tambah() takes 1 positional argument but 2 were given` | Lupa menulis `self` di definisi method | Tambah `self` sebagai parameter pertama di semua method di dalam class |
| `NameError: name 'daftar' is not defined` | Di dalam class menulis `daftar`, bukan `self.daftar` | Ganti menjadi `self.daftar` |
| `AttributeError: 'PengelolaTugas' object has no attribute 'daftar'` | `__init__` tidak membuat `self.daftar` (salah ketik nama atau jorokan) | Cek method `__init__`: dua garis bawah di tiap sisi, dan isinya menjorok 8 spasi |
| Daftar tampil sebagai `<tugas.Tugas object at 0x...>` | Method `__str__` salah ketik | Pastikan namanya persis `__str__` (dua garis bawah di kiri dan kanan) |
| `IndentationError` | Method harus menjorok 4 spasi di dalam class, isi method 8 spasi | Rapikan jorokan baris yang disebut error |
| Prompt Python interaktif berubah menjadi `...` | Ada kurung atau tanda kutip yang belum ditutup | Tekan Ctrl+C, lalu ulangi barisnya |
| Terjebak di `>>>` | Python interaktif belum ditutup | Ketik `exit()` lalu Enter |
| `fatal: The current branch main has no upstream branch` | Push pertama belum pernah memakai `-u` | `git push -u origin main` |
| Folder `__pycache__` muncul | Python menyimpan hasil kompilasi modul | Normal. Abaikan, Git sudah mengabaikannya |

### Jalur kejar

Tertinggal beberapa bagian? Tidak perlu mengetik ulang semuanya. Salin file lengkap dari **bagian terakhir yang berhasil kamu selesaikan**:

| Posisi terakhirmu | Salin ke `tugas.py` | Salin ke `main.py` |
| --- | --- | --- |
| Belum selesai Bagian B | **Isi lengkap tugas.py setelah bagian B** | **Isi lengkap main.py setelah bagian B** |
| Selesai B, belum C | **Isi lengkap tugas.py setelah bagian C** | (tetap versi B) |
| Selesai C, belum D | **Isi lengkap tugas.py setelah bagian D** | **Isi lengkap main.py setelah bagian D** |

Caranya: buka file di VS Code, Ctrl+A, Delete, tempel, Ctrl+S, lalu `uv run main.py`. Setelah itu lanjut ke bagian berikutnya. Tanyakan arti kodenya ke temanmu atau trainer setelah kamu mengejar.
