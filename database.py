import sqlite3
import os

DB_PATH = os.path.join("data", "attendance.db")

def get_db():
    return sqlite3.connect(DB_PATH)

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        roll_no TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        encoding BLOB NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        roll_no TEXT,
        date TEXT,
        time TEXT
    )
    """)

    conn.commit()
    conn.close()
