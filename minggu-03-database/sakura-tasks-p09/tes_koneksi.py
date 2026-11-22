from db import fetch_all

for baris in fetch_all("SELECT COUNT(*) AS total FROM tasks"):
    print("Jumlah tugas:", baris["total"]) 