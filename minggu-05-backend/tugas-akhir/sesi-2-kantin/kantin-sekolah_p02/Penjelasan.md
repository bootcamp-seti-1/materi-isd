# Memahami Proyek API Kantin Sekolah

Dokumen ini menjelaskan **tujuan proyek, progres, alur data, aturan bisnis, dan fungsi kode** berdasarkan README serta isi file yang diperiksa. Fokus pembahasan kode ada di tiga file yang dilengkapi untuk tugas: `schemas.py`, `routers/menus.py`, dan `routers/orders.py`.

## 1. Tujuan proyek dan progres saat ini

### Tujuan

Sekolah ingin siswa memesan makanan lewat aplikasi. Aplikasi tersebut membutuhkan API untuk membaca menu, membuat pesanan, melihat pesanan, membatalkan pesanan, dan melihat ringkasan penjualan. API ini menggunakan FastAPI, sedangkan menu dan pesanan disimpan di MySQL.

Bayangkan alur singkatnya:

> Siswa memilih menu → API memeriksa input dan stok → API menyimpan pesanan dan mengurangi stok → aplikasi menerima nomor serta detail pesanan.

### Progres kode saat ini

```text
Validasi request di schemas.py       [██████████] Sudah ditulis
Endpoint menu di routers/menus.py    [██████████] GET, POST, PATCH sudah ditulis
Endpoint order di routers/orders.py [██████████] Inti dan bonus sudah ditulis
Uji langsung dengan MySQL/server    [░░░░░░░░░░] Belum dipastikan
```

Baris penuh berarti implementasinya ada di kode, **bukan bukti bahwa ia sudah lulus pengujian**. README menyatakan tidak ada alat cek otomatis dan pekerjaan harus diperiksa manual.

## 2. Peta proyek: siapa memanggil siapa?

```text
Aplikasi / browser / curl
          │ mengirim HTTP request
          ▼
       main.py
          │ memasang router
          ├── routers/menus.py ──┐
          └── routers/orders.py ─┤
                                 ├── schemas.py (validasi/bentuk data)
                                 └── db.py (query MySQL)
                                           │
                                           ▼
                               kantin_menus, kantin_orders
```

Urutan umum saat request:

1. FastAPI menerima URL dan body JSON.
2. Jika ada body, Pydantic memeriksa body memakai model di `schemas.py`. Input yang salah biasanya dihentikan dengan `422` sebelum fungsi route berjalan.
3. Route menjalankan aturan bisnis, misalnya mencari menu atau membandingkan stok.
4. Route membaca/mengubah database lewat helper `db.py`.
5. Hasil dikembalikan sesuai `response_model`, misalnya `Menu` atau `Order`.

## 3. File dan data database

| File | Fungsi |
|---|---|
| `main.py` | Membuat aplikasi FastAPI, mendaftarkan router, dan menangani error MySQL. |
| `schemas.py` | Menentukan bentuk request/response dan validasi input. |
| `routers/menus.py` | Semua endpoint yang berhubungan dengan menu. |
| `routers/orders.py` | Semua endpoint order dan laporan. |
| `aturan.py` | Menyimpan angka aturan agar schema dan hitungan memakai sumber yang sama. |
| `db.py` | Membuka koneksi MySQL dan menyediakan helper query. |
| `db/schema.sql` | Menghapus lalu membuat tabel kantin. |
| `db/seed.sql` | Mengisi enam menu awal. |
| `pyproject.toml` | Menentukan Python minimal 3.12 dan dependensi FastAPI/MySQL. |
| `.python-version` | Memilih Python 3.12 untuk lingkungan proyek. |
| `.gitignore` | Mengabaikan `.env`, `.venv`, dan cache Python. |
| `routers/__init__.py` | File kosong penanda bahwa `routers` adalah package Python; tidak menjalankan aturan bisnis. |

### Dua tabel

**`kantin_menus`** menyimpan `id`, `name`, `category`, `price`, `stock`, dan `created_at`.

**`kantin_orders`** menyimpan `id`, `menu_id`, `qty`, `total`, `status`, dan `created_at`. `menu_id` menunjuk ke `kantin_menus.id`, jadi setiap order berkaitan dengan menu yang dipesan. Status database hanya `baru` atau `batal`.

Data awal dari `seed.sql`: Nasi Goreng (stok 20), Mi Ayam (15), Roti Bakar (0), Es Teh (50), Jus Jeruk (10), Air Mineral (30). Tabel order awalnya kosong.

## 4. Aturan bisnis dari README

### Validasi input menu

- `name`: trim spasi pinggir, lalu panjangnya 3–50 karakter.
- `category`: hanya `makanan` atau `minuman`.
- `price`: 1000–50000 dan kelipatan 500.
- `stock`: 0–200; pada POST jika tidak dikirim nilainya 0.
- Field yang tidak dikenal ditolak.
- Kegagalan validasi request menghasilkan `422`.

### Validasi input order

- `menu_id` harus lebih dari 0.
- `qty` harus 1–10.
- Field yang tidak dikenal ditolak.
- Kegagalan validasi request menghasilkan `422`.

### Hasil yang diwajibkan

| Aksi | Urutan dan hasil |
|---|---|
| POST menu | Nama kembar tanpa membedakan kapitalisasi → `409`, `Nama menu sudah ada`; jika lolos, simpan dan balas `201`. |
| PATCH menu | Cari menu (`404`) → tolak field terkirim yang bernilai `null` (`422`) → cek nama terhadap menu lain (`409`) → ubah field yang dikirim (`200`). |
| POST order | Cari menu (`400`, `Menu tidak ditemukan`) → cek stok (`409`, `Stok tidak cukup`) → hitung total → kurangi stok dan simpan order `baru` (`201`). Dua kegagalan pertama tidak boleh mengubah data. |
| GET detail order | Jika order tidak ada, balas `404`. |
| Batalkan order | Cari order (`404`) → jika sudah `batal`, `409` dengan `Pesanan sudah dibatalkan` → ubah status dan kembalikan stok (`200`). Pembatalan kedua tidak boleh mengembalikan stok lagi. |
| GET daftar order | Urut `id`; filter `status` jika diminta. |
| GET laporan | Hitung jumlah dan pendapatan dari order `baru` saja; jika belum ada, hasilnya 0 dan 0. |

Diskon order dihitung dari **subtotal** (`harga × qty`), bukan harga satuan. Jika subtotal mencapai batas diskon atau lebih, total dikurangi persentase diskon. Contoh: subtotal 70000 menjadi 63000.

## 5. Penjelasan rinci `schemas.py`

File ini seperti penjaga pintu: request yang bentuk atau nilainya salah ditolak sebelum menyentuh database.

### Import dan tipe pilihan

- `BaseModel` adalah dasar model Pydantic.
- `Field` menambahkan batas nilai, misalnya minimum dan maksimum.
- `field_validator` menjalankan pemeriksaan/penyesuaian khusus, di sini untuk memangkas nama.
- `ConfigDict(extra="forbid")` berarti key tambahan dalam JSON ditolak.
- `import aturan` memungkinkan kode memakai angka seperti `aturan.HARGA_MIN`.
- `Kategori = Literal["makanan", "minuman"]` membatasi kategori ke dua pilihan itu.
- `StatusPesanan = Literal["baru", "batal"]` membatasi status response/order ke dua nilai itu.

### `MenuCreate`

Model ini dipakai body `POST /v1/menus`.

- `name` harus berada dalam batas panjang dari `aturan.py`.
- Validator mode `before` menjalankan `strip()` sebelum panjang diperiksa. Jadi `"  Es Teh  "` menjadi `"Es Teh"`.
- `category` harus cocok dengan `Kategori`.
- `price` harus memenuhi batas bawah, batas atas, dan kelipatan harga.
- `stock` default ke 0, dengan batas 0 sampai `STOK_MAX`.
- `extra="forbid"` menolak key seperti `"warna": "merah"`.

### `MenuUpdate`

Model ini dipakai body PATCH. Field boleh tidak disertakan karena PATCH hanya mengubah sebagian data. Contoh `{"price": 11000}` berarti hanya harga yang diminta untuk berubah.

Field bertipe `... | None` agar field yang tidak dikirim punya nilai default `None`, dan `null` yang dikirim bisa dikenali route. `body.model_dump(exclude_unset=True)` di route membedakan:

- body `{}` → tidak ada field yang dikirim;
- body `{"price": null}` → field `price` dikirim secara eksplisit dengan `null`.

README meminta menu dicari sebelum pemeriksaan `null`, karena itu `null` tidak langsung ditolak schema; route yang menolaknya setelah pencarian menu.

### `OrderCreate`

Model body `POST /v1/orders`. `menu_id` harus positif dan `qty` harus berada dalam batas `QTY_MIN`–`QTY_MAX`. Field lain ditolak.

### Model response

- `Menu`: bentuk data menu, termasuk ID dan waktu dibuat.
- `Order`: bentuk data pesanan, termasuk ID, menu, jumlah, total, status, dan waktu dibuat.
- `Laporan`: dua angka, yaitu jumlah pesanan dan pendapatan.

Model-model response ini dipasang di router melalui `response_model`. FastAPI memeriksa hasil route agar bentuk JSON keluar sesuai schema.

## 6. Penjelasan rinci `routers/menus.py`

Router ini memiliki awalan `/v1/menus`. Misalnya route `@router.get("")` menjadi `GET /v1/menus`.

### `KOLOM` dan `cari_menu`

`KOLOM` adalah daftar kolom menu yang dibutuhkan response. `cari_menu(menu_id)` mencari satu menu menggunakan parameter SQL. Jika tidak ada, helper ini melempar `404`. Ia dipakai oleh endpoint detail dan sesudah insert/update untuk mengambil data lengkap.

### `daftar_menu`

`GET /v1/menus`:

1. Menerima kategori, limit, dan offset.
2. Jika kategori diberikan, menambahkan kondisi `category = %s`.
3. Mengurutkan hasil berdasarkan `id`.
4. Menggunakan limit/offset untuk pagination.

Nilai request dikirim sebagai parameter SQL; teks input tidak ditempel langsung ke query.

### `detail_menu`

`GET /v1/menus/{menu_id}` hanya memanggil `cari_menu`. Karena itu perilaku `404` berada di satu helper yang dapat digunakan ulang.

### `buat_menu`

`POST /v1/menus`:

1. Mengambil nama dari body dan membuang spasi pinggir.
2. Query `LOWER(TRIM(name)) = LOWER(TRIM(%s))` mencari nama yang sama tanpa membedakan kapitalisasi/spasi pinggir.
3. Jika hasil query ada, route melempar `409` dengan pesan yang diwajibkan.
4. Jika tidak ada, `insert()` menyimpan nama, kategori, harga, dan stok. Nilai-nilai query dikirim sebagai parameter.
5. Helper insert memberi ID baru; `cari_menu()` mengambil ulang seluruh kolom untuk response.

Decorator route menetapkan response model `Menu` dan status sukses `201`.

### `ubah_menu`

`PATCH /v1/menus/{menu_id}` mengikuti urutan tugas:

1. `cari_menu()` memastikan ID ada terlebih dahulu. Jadi ID tidak ada menjadi `404`, bahkan jika body berisi `null`.
2. `model_dump(exclude_unset=True)` mengambil hanya field yang benar-benar dikirim.
3. Jika salah satu field yang dikirim bernilai `None`, route menjawab `422`.
4. Jika `name` dikirim, route mencari nama yang sama pada menu **lain**. `id <> %s` mengecualikan menu yang sedang diedit. Duplikat menghasilkan `409`.
5. `kolom_diizinkan` membatasi kolom yang boleh diperbarui ke `name`, `category`, `price`, dan `stock`.
6. Route membangun bagian `SET` hanya dari kolom yang diizinkan, mengirim nilainya sebagai parameter, lalu memanggil `execute()`.
7. `cari_menu()` mengambil ulang data terbaru; response sukses default-nya `200`.

Jika body kosong, tidak ada kolom untuk di-update, sehingga route mengembalikan menu saat ini tanpa menjalankan UPDATE. README tidak menentukan kasus body kosong; ini diperlakukan sebagai no-op.

## 7. Penjelasan rinci `routers/orders.py`

Router order berawalan `/v1/orders`; router laporan terpisah memakai `/v1/laporan`. `KOLOM` mencantumkan semua kolom response Order, termasuk `created_at`.

### `buat_pesanan`

`POST /v1/orders`:

1. Schema sudah memeriksa `menu_id`, `qty`, dan field tambahan.
2. Query mengambil harga dan stok menu.
3. Menu tidak ditemukan → `400`, `Menu tidak ditemukan`.
4. Stok lebih kecil dari qty → `409`, `Stok tidak cukup`.
5. Setelah kedua pemeriksaan lolos, subtotal dihitung: `price × qty`.
6. Jika subtotal mencapai ambang, kode memakai hitungan integer untuk memotong diskon; jika tidak, total sama dengan subtotal.
7. `execute()` mengurangi stok.
8. `insert()` menyimpan order dengan status `"baru"` dan mengembalikan ID order.
9. Query mengambil semua kolom order baru untuk response `201`.

Contoh: Es Teh (3000) × 2 = subtotal dan total 6000; stok 50 menjadi 48. Nasi Goreng (12000) × 5 = subtotal 60000; setelah diskon 10%, total 54000.

### `detail_pesanan`

`GET /v1/orders/{order_id}` mencari order dan memilih kolom dari `KOLOM`. Jika tidak ditemukan, route menjawab `404`; jika ada, response menyertakan seluruh field model `Order`.

### `batalkan_pesanan`

`POST /v1/orders/{order_id}/batal`:

1. Cari order. Tidak ada → `404`.
2. Jika status sudah `batal`, jawab `409` dan berhenti. Karena stok belum disentuh, pembatalan kedua tidak menambah stok lagi.
3. Ubah status order menjadi `batal`.
4. Tambahkan `qty` order ke stok menu yang tersimpan di order.
5. Panggil `detail_pesanan()` untuk mengambil order terbaru dan mengembalikannya dengan status HTTP `200`.

### `daftar_pesanan`

`GET /v1/orders` mengambil semua order dan mengurutkannya berdasarkan ID. Jika query `?status=baru` atau `?status=batal` diberikan, query SQL menambahkan filter status. Tipe `StatusPesanan` membatasi nilai status yang diterima.

### `laporan`

`GET /v1/laporan` menggunakan query agregat:

- `COUNT(*)` menghitung order berstatus `baru`.
- `SUM(total)` menjumlah pendapatan dari order tersebut.
- `COALESCE(..., 0)` mengubah hasil SUM kosong dari `null` menjadi 0.
- Nilai dikonversi ke integer lalu dikemas sebagai `Laporan`.

Order batal tidak masuk hitungan karena query hanya memilih status `baru`.

Di bagian atas file masih ada komentar `TODO` lama yang menjadi pemisah bagian. Berdasarkan kode yang diperiksa, fungsi-fungsi inti dan bonus di bawahnya sudah diisi; status terakhir sebaiknya dinilai dari isi fungsi, bukan komentar lama itu.

## 8. Penjelasan file pendukung

### `main.py`

Membuat aplikasi FastAPI, memberi judul dan versi, menyediakan `GET /`, lalu memasang router menu, order, dan laporan. Handler MySQL mengubah error database menjadi status `500` dan pesan umum. Error bisnis seperti `404`/`409` berasal dari route, bukan handler tersebut.

### `aturan.py`

Berisi angka terpusat: panjang nama, batas harga, kelipatan harga, stok maksimum, qty, batas diskon, dan persentase diskon. Schema dan route menggunakan konstanta ini supaya angka bisnis konsisten.

### `db.py`

`DB_CONFIG` membaca kredensial database dari environment (`.env` saat server dijalankan dengan opsi `--env-file`).

- `fetch_all`: jalankan SELECT dan hasilkan semua baris sebagai dictionary.
- `fetch_one`: gunakan `fetch_all`, lalu hasilkan baris pertama atau `None`.
- `execute`: jalankan UPDATE/DELETE dan commit.
- `insert`: jalankan INSERT, commit, lalu berikan ID yang dibuat.

Setiap pemanggilan helper membuka dan menutup koneksi sendiri. `execute()` dan `insert()` commit masing-masing, jadi rangkaian beberapa perubahan bukan satu transaksi bersama. Jika database gagal di tengah rangkaian sukses, perubahan pertama bisa sudah tersimpan.

### SQL dan konfigurasi

`schema.sql` menghapus tabel lama lalu membuat ulang tabel beserta foreign key. Karena itu menjalankannya menghapus data lama. `seed.sql` mengisi enam menu awal. README menyebut menyalin `.env.example` menjadi `.env`, tetapi `.env.example` tidak ditemukan di folder ketika file diperiksa; ikuti instruksi trainer/siapkan konfigurasi sesuai README sebelum menjalankan API. `.gitignore` menyatakan `.env` jangan dimasukkan ke Git.

## 9. Cara menjalankan dan menguji

README memberi instruksi untuk menyiapkan MySQL dan `.env`, menjalankan `schema.sql` lalu `seed.sql`, kemudian menjalankan server:

```text
uv run --env-file .env fastapi dev main.py
```

Buka `http://localhost:8000/docs`, lalu gunakan tombol **Try it out**. Uji hasil HTTP **dan** kondisi database:

1. `GET /v1/menus`: harus berisi enam menu awal.
2. POST menu baru: harus `201`; ulangi dengan nama sama tapi kapitalisasi berbeda: harus `409`.
3. PATCH satu field: pastikan field lain tetap. Coba ID tak ada dan `null` untuk melihat urutan `404` lalu `422`.
4. POST order `menu_id=4, qty=2`: total 6000; stok Es Teh turun dua.
5. Coba menu tak ada (`400`), stok tidak cukup (`409`), dan subtotal tepat/di atas ambang diskon.
6. Ambil detail order, batalkan, lalu batalkan lagi. Pembatalan kedua harus `409` dan stok tidak boleh bertambah lagi.
7. Daftar order tanpa filter dan dengan filter status. Buat order aktif dan batal; laporan hanya menghitung yang aktif.

Setiap POST/PATCH/pembatalan bisa mengubah database. Reset dengan schema lalu seed hanya pada database tugas yang benar. Penilaian README dimulai dari data awal.

## 10. Batas kepastian

Uraian ini menjelaskan kode yang ada, tetapi server dan MySQL belum dijalankan untuk memverifikasi perilaku end-to-end. Contoh uji di atas adalah hasil yang seharusnya terlihat menurut aturan, bukan klaim bahwa pengujian sudah lulus. README juga mengingatkan agar pekerjaan dikumpulkan di branch pribadi, bukan `main`.

## 11. Belajar membaca `schemas.py` lewat potongan kode

Bagian ini sengaja mengulang hal penting dengan melihat bentuk kode aslinya. Anggap schema sebagai **pemeriksa formulir**: sebelum data diserahkan ke route, schema memastikan pengguna mengisi nilai yang boleh.

### 11.1 Alias kategori dan status

```python
Kategori = Literal["makanan", "minuman"]
StatusPesanan = Literal["baru", "batal"]
```

`Literal` adalah cara menyatakan pilihan yang diizinkan. Jadi:

- `Kategori` menerima `"makanan"` atau `"minuman"` saja.
- `StatusPesanan` menerima `"baru"` atau `"batal"` saja.

Nama `Kategori` ini sudah ada di kerangka awal proyek; bukan tabel database atau endpoint baru. Model input dan response memakai tipe ini agar kategori/status tidak berisi sembarang teks.

### 11.2 `MenuCreate`: formulir untuk menambah menu

```python
class MenuCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(
        min_length=aturan.NAMA_MIN,
        max_length=aturan.NAMA_MAX,
    )
    category: Kategori
    price: int = Field(
        ge=aturan.HARGA_MIN,
        le=aturan.HARGA_MAX,
        multiple_of=aturan.KELIPATAN_HARGA,
    )
    stock: int = Field(default=0, ge=0, le=aturan.STOK_MAX)

    @field_validator("name", mode="before")
    @classmethod
    def trim_name(cls, value):
        return value.strip() if isinstance(value, str) else value
```

Cara membacanya:

1. `class MenuCreate(BaseModel)` berarti kita membuat model request bernama `MenuCreate` berdasarkan kemampuan Pydantic.
2. `model_config = ConfigDict(extra="forbid")` berarti key yang tidak didefinisikan akan ditolak. Contoh body dengan `"warna": "merah"` tidak boleh diam-diam diterima.
3. `name: str` berarti nama harus berupa teks.
4. `Field(min_length=..., max_length=...)` membatasi panjang. Nilai angka berasal dari `aturan.py`, bukan disalin ke schema.
5. `category: Kategori` menggunakan pilihan kategori yang dijelaskan tadi.
6. `price: int` berarti harga bilangan bulat. `ge` adalah batas minimal, `le` batas maksimal, dan `multiple_of` berarti harga harus kelipatan tertentu.
7. `stock` juga bilangan bulat. `default=0` dipakai jika klien tidak mengirim stok. `ge=0` menyatakan stok tidak boleh negatif; `aturan.py` menyediakan batas maksimumnya, tetapi tidak menyediakan konstanta batas minimum.
8. `field_validator("name", mode="before")` meminta Pydantic menjalankan fungsi validator untuk field `name` sebelum validasi panjang.
9. `@classmethod` adalah cara Pydantic memanggil validator sebagai bagian dari model.
10. Baris `value.strip()` membuang spasi hanya di bagian awal/akhir. Pemeriksaan `isinstance` memastikan `.strip()` hanya dipanggil pada teks.

Misalnya body memiliki nama `"  Es Teh  "`. Validator mengubahnya menjadi `"Es Teh"`, baru kemudian Pydantic menguji panjangnya. Nama yang hanya berisi spasi menjadi teks kosong sesudah trim dan gagal batas panjang.

### 11.3 `MenuUpdate`: formulir untuk PATCH

```python
class MenuUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str | None = Field(
        default=None,
        min_length=aturan.NAMA_MIN,
        max_length=aturan.NAMA_MAX,
    )
    category: Kategori | None = None
    price: int | None = Field(
        default=None,
        ge=aturan.HARGA_MIN,
        le=aturan.HARGA_MAX,
        multiple_of=aturan.KELIPATAN_HARGA,
    )
    stock: int | None = Field(
        default=None,
        ge=0,
        le=aturan.STOK_MAX,
    )
```

Tanda `| None` berarti nilai boleh berupa tipe normalnya atau `None` (Python yang mewakili JSON `null`). Default `None` berarti field itu boleh tidak dikirim. Inilah yang membuat PATCH berbeda dari POST: pada PATCH, klien boleh hanya mengirim satu field.

Contoh:

```json
{"price": 11000}
```

Artinya hanya harga yang diminta berubah. Tidak berarti `name`, `category`, dan `stock` harus diganti menjadi `None`.

Mengapa `null` belum langsung ditolak schema? README mewajibkan urutan PATCH: cari menu dulu, baru periksa `null`. Kalau menu tidak ada dan body berisi `null`, hasil yang harus menang adalah `404`, bukan `422`. Maka schema membiarkan `null` sampai route; route memeriksanya sesuai urutan.

Validator nama yang sama dipakai di `MenuUpdate`. Jadi jika PATCH berisi nama, spasinya dibuang sebelum nama diproses.

### 11.4 `OrderCreate`: formulir untuk order

```python
class OrderCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    menu_id: int = Field(gt=0)
    qty: int = Field(ge=aturan.QTY_MIN, le=aturan.QTY_MAX)
```

- `menu_id: int` harus bilangan bulat dan `gt=0` berarti lebih besar dari nol.
- `qty` memakai batas minimum/maksimum dari `aturan.py`.
- Key lain ditolak karena `extra="forbid"`.

Jika body salah, fungsi `buat_pesanan` belum berjalan. FastAPI/Pydantic menghentikan request dengan `422`.

### 11.5 Model response

```python
class Menu(BaseModel):
    id: int
    name: str
    category: Kategori
    price: int
    stock: int
    created_at: datetime

class Order(BaseModel):
    id: int
    menu_id: int
    qty: int
    total: int
    status: StatusPesanan
    created_at: datetime

class Laporan(BaseModel):
    jumlah_pesanan: int
    pendapatan: int
```

Model-model ini adalah bentuk **data keluar**. Contoh, karena `Order` meminta `created_at`, query detail order harus mengambil kolom itu. Jika kolom yang dikembalikan tidak cocok, FastAPI dapat melaporkan response tidak sesuai model.

## 12. Belajar membaca `routers/menus.py`

### 12.1 Router dan daftar kolom

```python
router = APIRouter(prefix="/v1/menus", tags=["menus"])
KOLOM = "id, name, category, price, stock, created_at"
```

`APIRouter` mengelompokkan endpoint. Karena prefix-nya `/v1/menus`, dekorator `@router.get("")` menjadi `GET /v1/menus`, sedangkan `@router.get("/{menu_id}")` menjadi `GET /v1/menus/{menu_id}`. `KOLOM` menghindari penulisan daftar kolom yang sama berulang kali.

### 12.2 Helper `cari_menu`

```python
def cari_menu(menu_id: int) -> dict:
    menu = fetch_one(
        f"SELECT {KOLOM} FROM kantin_menus WHERE id = %s",
        (menu_id,),
    )
    if menu is None:
        raise HTTPException(
            status_code=404,
            detail=f"Menu {menu_id} tidak ditemukan",
        )
    return menu
```

`fetch_one` menjalankan SELECT dan menghasilkan satu baris atau `None`. Tanda `%s` adalah tempat nilai parameter untuk MySQL Connector; `(menu_id,)` adalah tuple yang memasok nilainya. Koma setelah `menu_id` membuatnya tuple satu elemen.

Jika baris tidak ditemukan, `raise HTTPException(...)` menghentikan fungsi dan FastAPI membentuk response error. Kalau ada, dictionary baris menu dikembalikan.

### 12.3 Daftar dan detail menu

```python
@router.get("", response_model=list[Menu])
def daftar_menu(
    category: Kategori | None = None,
    limit: int = Query(default=10, ge=1, le=50),
    offset: int = Query(default=0, ge=0),
):
    syarat = []
    params = []
    if category is not None:
        syarat.append("category = %s")
        params.append(category)
    where = f"WHERE {' AND '.join(syarat)}" if syarat else ""
    sql = f"SELECT {KOLOM} FROM kantin_menus {where} ORDER BY id LIMIT %s OFFSET %s"
    params += [limit, offset]
    return fetch_all(sql, tuple(params))
```

- `response_model=list[Menu]` mengatakan hasil harus berupa daftar menu.
- `category` boleh kosong; `limit` default 10 dan dibatasi 1–50; `offset` default 0 dan tidak boleh negatif.
- `syarat` menampung kondisi SQL. Tanpa kategori, `WHERE` tidak diperlukan. Dengan kategori, query hanya mengambil kategori itu.
- `params` menyimpan nilai untuk placeholder `%s`, terpisah dari teks SQL.
- `ORDER BY id` membuat urutan stabil; `LIMIT` dan `OFFSET` mengatur halaman data.

Detail menu hanya memakai helper:

```python
@router.get("/{menu_id}", response_model=Menu)
def detail_menu(menu_id: int):
    return cari_menu(menu_id)
```

### 12.4 POST menu: cek duplikat lalu simpan

```python
@router.post("", response_model=Menu, status_code=201)
def buat_menu(body: MenuCreate):
    nama = body.name.strip()
    duplikat = fetch_one(
        "SELECT id FROM kantin_menus "
        "WHERE LOWER(TRIM(name)) = LOWER(TRIM(%s))",
        (nama,),
    )
    if duplikat is not None:
        raise HTTPException(status_code=409, detail="Nama menu sudah ada")

    menu_id = insert(
        "INSERT INTO kantin_menus (name, category, price, stock) "
        "VALUES (%s, %s, %s, %s)",
        (nama, body.category, body.price, body.stock),
    )
    return cari_menu(menu_id)
```

Baris per baris dalam bahasa sederhana:

1. `body: MenuCreate` membuat FastAPI memeriksa input memakai model `MenuCreate` sebelum masuk ke fungsi.
2. `nama = body.name.strip()` memastikan nama bersih. Schema juga melakukan trim; ini menjadi perlindungan tambahan di route.
3. Query pertama mencari nama yang sudah ada. `LOWER` mengubah huruf menjadi kecil; `TRIM` membuang spasi pinggir dari nama database dan input. Jadi `Nasi Goreng`, `nasi goreng`, dan input dengan spasi pinggir dianggap sama untuk pemeriksaan ini.
4. Jika query menghasilkan baris, `duplikat is not None`; route mengirim `409` dengan pesan yang harus persis.
5. Jika tidak ada duplikat, `insert()` menambah baris menu. Nilai body dikirim terpisah sebagai parameter, bukan ditempel ke teks query.
6. `insert()` mengembalikan ID baru. `cari_menu(menu_id)` mengambil ulang seluruh kolom agar response berisi ID dan `created_at`.
7. `status_code=201` pada dekorator menetapkan status sukses untuk menu baru.

**Contoh alur:** database sudah punya `Nasi Goreng`; request mengirim `" nasi goreng "`. Schema memangkas spasi, query membandingkan huruf kecil, menemukan baris yang ada, lalu berhenti dengan `409`. Insert tidak dijalankan.

### 12.5 PATCH menu: periksa urutan, update sebagian

```python
@router.patch("/{menu_id}", response_model=Menu)
def ubah_menu(menu_id: int, body: MenuUpdate):
    menu = cari_menu(menu_id)
    perubahan = body.model_dump(exclude_unset=True)

    if any(nilai is None for nilai in perubahan.values()):
        raise HTTPException(status_code=422, detail="Field tidak boleh null")

    if "name" in perubahan:
        nama = perubahan["name"].strip()
        duplikat = fetch_one(
            "SELECT id FROM kantin_menus "
            "WHERE LOWER(TRIM(name)) = LOWER(TRIM(%s)) AND id <> %s",
            (nama, menu_id),
        )
        if duplikat is not None:
            raise HTTPException(status_code=409, detail="Nama menu sudah ada")
        perubahan["name"] = nama

    kolom_diizinkan = ("name", "category", "price", "stock")
    kolom_diubah = [kolom for kolom in kolom_diizinkan if kolom in perubahan]
    if not kolom_diubah:
        return menu

    set_clause = ", ".join(f"{kolom} = %s" for kolom in kolom_diubah)
    params = tuple(perubahan[kolom] for kolom in kolom_diubah) + (menu_id,)
    execute(
        f"UPDATE kantin_menus SET {set_clause} WHERE id = %s",
        params,
    )
    return cari_menu(menu_id)
```

Pahami fungsi ini sebagai daftar pemeriksaan:

1. `cari_menu(menu_id)` dijalankan **pertama**. Jika ID tidak ada, hasil langsung `404`.
2. `model_dump(exclude_unset=True)` menghasilkan dictionary hanya dari field yang dikirim. Contoh body `{"price": 11000}` menghasilkan `{"price": 11000}`; `name`, `category`, dan `stock` tidak ikut di-update.
3. `any(... is None ...)` mencari apakah ada nilai `null` di antara field yang dikirim. Jika ada, hasil `422`.
4. Pengecekan nama dijalankan hanya jika pengguna mengirim nama. Kondisi `id <> %s` berarti “nama yang sama pada baris selain menu yang sedang diedit”. Mengganti nama menu menjadi nama yang sama dengan dirinya sendiri tidak dianggap duplikat.
5. `kolom_diizinkan` adalah daftar nama kolom yang boleh masuk ke UPDATE. Nilai yang dikirim pengguna hanya masuk sebagai parameter; nama kolom dipilih dari daftar tetap.
6. `set_clause` menyusun bagian SQL yang berubah. Untuk body `{"price": 11000}`, hasil konsepnya `price = %s WHERE id = %s`, dengan parameter `(11000, menu_id)`.
7. `execute()` menjalankan UPDATE. `cari_menu()` mengambil ulang baris terbaru untuk response `200`.
8. Jika tidak ada field yang dikirim, `kolom_diubah` kosong dan fungsi mengembalikan menu lama. Ini perilaku no-op karena README tidak menetapkan aturan khusus untuk body kosong.

## 13. Belajar membaca `routers/orders.py`

### 13.1 Router order dan daftar kolom

```python
router = APIRouter(prefix="/v1/orders", tags=["orders"])
laporan_router = APIRouter(prefix="/v1/laporan", tags=["laporan"])
KOLOM = "id, menu_id, qty, total, status, created_at"
```

Ada dua kelompok URL: `/v1/orders` untuk order dan `/v1/laporan` untuk ringkasan penjualan. Kolom `KOLOM` memastikan query detail, pembatalan, dan response order mengambil semua field yang dibutuhkan schema `Order`.

### 13.2 POST order: satu alur dari awal sampai akhir

```python
@router.post("", response_model=Order, status_code=201)
def buat_pesanan(body: OrderCreate):
    menu = fetch_one(
        "SELECT id, price, stock FROM kantin_menus WHERE id = %s",
        (body.menu_id,),
    )
    if menu is None:
        raise HTTPException(status_code=400, detail="Menu tidak ditemukan")

    if menu["stock"] < body.qty:
        raise HTTPException(status_code=409, detail="Stok tidak cukup")

    subtotal = menu["price"] * body.qty
    total = subtotal
    if subtotal >= aturan.BATAS_DISKON:
        total = subtotal * (100 - aturan.DISKON_PERSEN) // 100

    execute(
        "UPDATE kantin_menus SET stock = stock - %s WHERE id = %s",
        (body.qty, body.menu_id),
    )
    order_id = insert(
        "INSERT INTO kantin_orders (menu_id, qty, total, status) "
        "VALUES (%s, %s, %s, %s)",
        (body.menu_id, body.qty, total, "baru"),
    )

    order = fetch_one(
        f"SELECT {KOLOM} FROM kantin_orders WHERE id = %s",
        (order_id,),
    )
    if order is None:
        raise HTTPException(
            status_code=500,
            detail="Pesanan tersimpan tetapi tidak dapat dibaca",
        )
    return order
```

Urutan ini penting; baca dari atas ke bawah:

1. `body: OrderCreate` berarti body diperiksa dulu. `menu_id` yang tidak positif, `qty` di luar batas, atau field asing ditolak `422` sebelum query menu.
2. SELECT mengambil menu sesuai ID yang diminta.
3. Jika tidak ada baris, tidak ada stok atau order yang diubah. Route berhenti dengan `400`.
4. Jika stok kurang dari qty, route berhenti dengan `409`. Pemeriksaan ini masih terjadi sebelum UPDATE/INSERT.
5. `subtotal` adalah harga menu dikali jumlah yang dibeli.
6. `total` awalnya sama dengan subtotal. Jika subtotal sudah mencapai ambang, kode mengalikan dengan sisa persentase setelah diskon. `// 100` adalah pembagian bulat supaya hasil tetap integer.
7. `execute()` mengurangi stok.
8. `insert()` menambah order dengan status `"baru"` dan memberikan ID order yang baru.
9. SELECT terakhir mengambil order lengkap, termasuk `created_at`. Jika tidak terbaca, kode memberi error `500` secara eksplisit; jika terbaca, response model `Order` membentuk response `201`.

Contoh dengan seed: Es Teh harganya 3000 dan stoknya 50. Body `{"menu_id": 4, "qty": 2}` menghasilkan subtotal 6000, tanpa diskon; stok menjadi 48. Nasi Goreng 12000 × 5 menghasilkan subtotal 60000; karena melewati ambang 50000, total menjadi 54000.

### 13.3 GET detail order

```python
@router.get("/{order_id}", response_model=Order)
def detail_pesanan(order_id: int):
    order = fetch_one(
        f"SELECT {KOLOM} FROM kantin_orders WHERE id = %s",
        (order_id,),
    )
    if order is None:
        raise HTTPException(
            status_code=404,
            detail=f"Pesanan {order_id} tidak ditemukan",
        )
    return order
```

Route mencari satu order. Tidak ada → `404`; ada → kembalikan dictionary hasil query. `response_model=Order` membuat FastAPI memeriksa bentuk response. `KOLOM` juga mengambil tanggal/waktu order yang diminta schema.

### 13.4 Membatalkan order

```python
@router.post("/{order_id}/batal", response_model=Order)
def batalkan_pesanan(order_id: int):
    order = fetch_one(
        f"SELECT {KOLOM} FROM kantin_orders WHERE id = %s",
        (order_id,),
    )
    if order is None:
        raise HTTPException(
            status_code=404,
            detail=f"Pesanan {order_id} tidak ditemukan",
        )

    if order["status"] == "batal":
        raise HTTPException(status_code=409, detail="Pesanan sudah dibatalkan")

    execute(
        "UPDATE kantin_orders SET status = %s WHERE id = %s",
        ("batal", order_id),
    )
    execute(
        "UPDATE kantin_menus SET stock = stock + %s WHERE id = %s",
        (order["qty"], order["menu_id"]),
    )
    return detail_pesanan(order_id)
```

- Query pertama harus berhasil menemukan order sebelum perubahan apa pun.
- Kondisi status batal dicek sebelum stok dikembalikan. Inilah yang mencegah pembatalan kedua menambah stok lagi.
- Jumlah stok yang dikembalikan diambil dari `order["qty"]`, bukan dari input baru, karena jumlah tersebut adalah jumlah yang benar-benar dipesan.
- Setelah status dan stok diperbarui, `detail_pesanan()` dipakai ulang untuk mengirim data terbaru. Status sukses default FastAPI untuk route ini adalah `200`.

### 13.5 Daftar order

```python
@router.get("", response_model=list[Order])
def daftar_pesanan(status: StatusPesanan | None = None):
    if status is None:
        return fetch_all(f"SELECT {KOLOM} FROM kantin_orders ORDER BY id")

    return fetch_all(
        f"SELECT {KOLOM} FROM kantin_orders WHERE status = %s ORDER BY id",
        (status,),
    )
```

Tanpa parameter status, query mengambil semua order. Dengan `?status=baru`, hanya order baru yang diambil; `?status=batal` hanya yang batal. Keduanya tetap diurutkan dengan ID. Parameter status divalidasi oleh tipe `StatusPesanan`.

### 13.6 Laporan

```python
@laporan_router.get("", response_model=Laporan)
def laporan():
    hasil = fetch_one(
        "SELECT COUNT(*) AS jumlah_pesanan, "
        "COALESCE(SUM(total), 0) AS pendapatan "
        "FROM kantin_orders WHERE status = %s",
        ("baru",),
    )
    return Laporan(
        jumlah_pesanan=int(hasil["jumlah_pesanan"]),
        pendapatan=int(hasil["pendapatan"]),
    )
```

- `WHERE status = %s` memastikan order batal tidak ikut dihitung.
- `COUNT(*)` menghitung banyaknya order aktif.
- `SUM(total)` menjumlah pendapatan.
- Jika belum ada order baru, `SUM` normalnya menghasilkan `NULL`; `COALESCE(..., 0)` menggantinya dengan angka nol.
- `int(...)` memastikan nilai yang dikirim sesuai tipe integer pada `Laporan`.

## 14. Bagaimana helper database menyambungkan route ke MySQL?

Potongan konsep dari `db.py`:

```python
def fetch_one(sql, params=()):
    rows = fetch_all(sql, params)
    return rows[0] if rows else None
```

Route seperti `cari_menu`, `detail_pesanan`, dan `buat_pesanan` memanggil `fetch_one`. Hasilnya dictionary satu baris, misalnya:

```python
{"id": 4, "price": 3000, "stock": 50}
```

Untuk perubahan data:

```python
execute("UPDATE ... WHERE id = %s", (nilai, id))
insert("INSERT ... VALUES (%s, ...)", (nilai, ...))
```

Helper menjalankan query dengan parameter, melakukan commit, lalu menutup koneksi. Jangan menaruh isi input pengguna langsung ke teks SQL; letakkan sebagai parameter seperti `%s`.

## 15. Latihan menelusuri satu skenario lengkap

Ambil data awal Es Teh: ID 4, harga 3000, stok 50.

Request:

```json
{"menu_id": 4, "qty": 2}
```

Telusuri dengan urutan ini:

1. Pydantic membentuk `OrderCreate`; ID positif dan qty 2 berada dalam batas.
2. `buat_pesanan()` meminta database mencari menu ID 4.
3. Menu ditemukan dan stok 50 tidak kurang dari qty 2.
4. Subtotal = 3000 × 2 = 6000. Nilai ini belum mencapai batas diskon, jadi total tetap 6000.
5. UPDATE membuat stok menjadi 48.
6. INSERT membuat order berstatus `baru`, qty 2, total 6000.
7. SELECT mengambil ID dan `created_at`; FastAPI mengirim response `Order` dengan status 201.

Sekarang misalkan order itu dibatalkan:

1. API mencari order tersebut; status masih `baru`.
2. Status diubah menjadi `batal`.
3. Stok Es Teh ditambah qty order, yaitu 2; stok kembali menjadi 50.
4. Detail terbaru dikembalikan dengan status HTTP 200.
5. Pembatalan ulang berhenti di pemeriksaan status dan menghasilkan 409; stok tetap 50.

Skenario ini menghubungkan schema, route, helper database, dua tabel, dan response API dalam satu cerita.

## 16. Hal yang perlu diingat saat belajar atau menjelaskan ke trainer

- **Schema** menjawab: “Apakah bentuk dan nilai input boleh?”.
- **Route** menjawab: “Apakah tindakan ini boleh menurut keadaan bisnis/database?”.
- **Database** menyimpan keadaan sebenarnya; perubahan stok dan status terlihat pada request berikutnya.
- **Status HTTP** menjelaskan hasil: 200 sukses biasa, 201 berhasil membuat data, 400/404 data yang dicari tidak ada sesuai aturan endpoint, 409 konflik bisnis, 422 input tidak valid, dan 500 masalah server/database.
- Pesan error tertentu di README harus sama persis.
- Implementasi semua fungsi terlihat pada kode, tetapi pengujian langsung masih perlu dilakukan. Jalankan kasus berhasil dan gagal, lalu periksa juga nilai stok, status, dan laporan.
