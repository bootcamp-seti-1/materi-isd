import subprocess, sys
from pathlib import Path

from db import get_connection


def reset_data(repo):
    """Kembalikan tabel koperasi ke data awal (schema.sql lalu seed.sql)."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        for nama in ("schema.sql", "seed.sql"):
            teks = (repo / "db" / nama).read_text(encoding="utf-8")
            for perintah in teks.split(";"):
                if perintah.strip():
                    cur.execute(perintah)
        conn.commit()
    finally:
        conn.close()


def jalankan(repo, teks):
    try:
        r = subprocess.run([sys.executable, "main.py"], cwd=repo, input=teks, capture_output=True,
                           text=True, timeout=20)
        return r.stdout, r.stderr
    except subprocess.TimeoutExpired:
        return "", "TIMEOUT"


def normal(s):
    return [b.rstrip() for b in s.rstrip().splitlines()]


def uji(repo, folder):
    hasil = []
    for masukan in sorted(folder.glob("*.in")):
        harap = masukan.with_suffix(".out").read_text(encoding="utf-8")
        reset_data(repo)
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
    print("Catatan: cek.py mengembalikan data koperasi ke data awal setiap kali jalan.")
