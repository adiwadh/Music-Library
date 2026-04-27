import sqlite3
import os

def get_db():
    if not os.path.exists("instance"):
        os.mkdir("instance")
    conn = sqlite3.connect("instance/music.db")
    conn.set_trace_callback(print)
    return conn

def create_tables():
    db = get_db()
    db.execute("""
    CREATE TABLE IF NOT EXISTS songs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        artist TEXT,
        url TEXT,
        is_favorite INTEGER DEFAULT 0
    )
    """)
    db.commit()
    db.close()
