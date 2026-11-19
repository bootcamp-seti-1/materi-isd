import mysql.connector

DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "sakura_p00",
    "password": "sakura123",
    "database": "sakura_db",
}


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def fetch_all(sql, params=()):
    conn = get_connection()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, params)
        return cur.fetchall()
    finally:
        conn.close()


def execute(sql, params=()):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        return cur.rowcount
    finally:
        conn.close()
