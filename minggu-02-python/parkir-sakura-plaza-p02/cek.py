import json, subprocess, sys
from pathlib import Path

# Folder yang diuji, dijalankan berurutan dari atas ke bawah.
# Setiap folder berisi pasangan berkas: NAMA.in (masukan) dan NAMA.out (harapan).
# Tambahkan baris baru di sini kalau kamu punya folder uji lain.
BAGIAN = [
    ("SKENARIO BAWAAN", "contoh"),
    ("SKENARIO BUATANKU", "contoh-saya"),
]

GARIS = "=" * 60


def jalankan(repo, teks):
    try:
        r = subprocess.run([sys.executable, "main.py"], cwd=repo, input=teks, capture_output=True,
                           text=True, timeout=10)
        return r.stdout, r.stderr
    except subprocess.TimeoutExpired:
        return "", "TIMEOUT"


def normal(s):
    return [b.rstrip() for b in s.rstrip().splitlines()]


def uji(repo, folder):
    hasil = []
    for masukan in sorted(folder.glob("*.in")):
        harap = masukan.with_suffix(".out").read_text(encoding="utf-8")
        out, err = jalankan(repo, masukan.read_text(encoding="utf-8"))
        hasil.append((masukan.stem, normal(out) == normal(harap), harap, out, err))
    return hasil


def jalankan_satu_bagian(repo, label, nama_folder):
    """Uji satu folder, cetak hasilnya, kembalikan (jumlah lulus, jumlah kasus)."""
    folder = repo / nama_folder
    print(GARIS)
    print(f"{label}  ({nama_folder}/)")
    print(GARIS)

    if not folder.is_dir():
        print(f"(folder {nama_folder}/ tidak ditemukan, dilewati)\n")
        return 0, 0

    hasil = uji(repo, folder)
    if not hasil:
        print("(tidak ada berkas .in di folder ini)\n")
        return 0, 0

    lulus = 0
    for nama, ok, harap, out, err in hasil:
        print(("LULUS  " if ok else "GAGAL  ") + nama)
        if ok:
            lulus += 1
            continue
        print("  seharusnya:")
        for b in (normal(harap) or ["(tidak mencetak apa pun)"]):
            print("    " + b)
        print("  programmu:")
        for b in (normal(out) or ["(tidak mencetak apa pun)"]):
            print("    " + b)
        if err.strip():
            print("  error: " + err.strip().splitlines()[-1])

    print(f"\n{lulus}/{len(hasil)} lulus\n")
    return lulus, len(hasil)


if __name__ == "__main__":
    repo = Path(__file__).resolve().parent

    total_lulus = 0
    total_kasus = 0
    for label, nama_folder in BAGIAN:
        lulus, jumlah = jalankan_satu_bagian(repo, label, nama_folder)
        total_lulus += lulus
        total_kasus += jumlah

    print(GARIS)
    print(f"TOTAL {total_lulus}/{total_kasus} lulus")
    print(GARIS)
    print("Buat skenariomu sendiri di folder contoh-saya/ (pasangan .in dan .out).")
