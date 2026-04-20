import sqlite3
import os

def get_db():
    if not os.path.exists("instance"):
        os.mkdir("instance")
    return sqlite3.connect("instance/music.db")

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
