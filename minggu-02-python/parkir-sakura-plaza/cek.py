import json, subprocess, sys
from pathlib import Path


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


if __name__ == "__main__":
    repo = Path(__file__).resolve().parent
    hasil = uji(repo, repo / "contoh")
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
    print(f"\n{lulus}/{len(hasil)} contoh lulus. Contoh ini hanya sebagian kecil dari yang diuji. Buat skenariomu sendiri.")
