import sqlite3

DB_PATH = "data/attendance.db"

def connect():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        emp_id TEXT PRIMARY KEY,
        name TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS embeddings (
        emp_id TEXT,
        embedding BLOB
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        emp_id TEXT,
        date TEXT,
        time TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()
