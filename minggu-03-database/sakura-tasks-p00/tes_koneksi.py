from db import fetch_all, get_connection, get_connection

conn = get_connection()
try:
    params=()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT COUNT(*) AS total FROM tasks", params)
    data =  cur.fetchall()
finally:
    conn.close()
    
for baris in data:
    print("Jumlah tugas:", baris["total"])
