import sqlite3

DB_PATH = "data/attendance.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT UNIQUE,
        name TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS encodings (
        student_id TEXT,
        encoding BLOB
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        student_id TEXT,
        date TEXT,
        time TEXT
    )
    """)

    conn.commit()
    conn.close()
